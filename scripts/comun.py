"""Lectura y validación compartidas: toda exportación pasa por estos controles."""
from collections import Counter
from datetime import date
from pathlib import Path
import csv
import hashlib
import json
import re
import unicodedata

RAIZ = Path(__file__).resolve().parents[1]
LOTE = ['id','nombre_crudo','nombre','tipo','homenaje','estado','nota','fuente']
CONFORMIDAD = ['id','nombre_crudo','nombre_aprobado','fecha','referencia']
TIPOS = {'calle','avenida','pasaje','camino','ruta','bulevar','diagonal'}
HOMENAJES = {'persona','lugar','fecha','otro'}

class DatosInvalidos(ValueError):
    pass

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def leer_csv(path, cabecera=None):
    try:
        with Path(path).open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f, strict=True)
            if cabecera is not None and reader.fieldnames != cabecera:
                raise DatosInvalidos(f'{Path(path).name}: cabecera exacta requerida: {",".join(cabecera)}')
            rows = list(reader)
        if any(None in r or any(v is None for v in r.values()) for r in rows):
            raise DatosInvalidos(f'{Path(path).name}: cantidad incorrecta de columnas')
        return rows
    except (OSError, UnicodeError, csv.Error) as e:
        raise DatosInvalidos(f'{Path(path).name}: {e}') from e

def escribir_csv(path, filas, campos):
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=campos,extrasaction='ignore'); w.writeheader(); w.writerows(filas)

def texto_cad(texto):
    if not texto or texto != texto.strip() or len(texto)>200:
        raise DatosInvalidos('el nombre debe tener 1–200 caracteres y no llevar espacios extremos')
    if any(c in texto for c in '|\\{}%'):
        raise DatosInvalidos('nombre con separador | o códigos CAD (\\, {, }, %); requiere revisión manual')
    if any(unicodedata.category(c).startswith('C') for c in texto):
        raise DatosInvalidos('nombre con caracteres de control o invisibles')
    try: texto.encode('cp1252',errors='strict')
    except UnicodeEncodeError as e:
        raise DatosInvalidos('nombre no representable en el auxiliar Windows-1252; no se sustituye por ?') from e

def cargar(raiz=RAIZ):
    raiz=Path(raiz); errores=[]
    manifest=json.loads((raiz/'datos/crudo/manifest.json').read_text())
    for name in ('calles_crudo.csv','etiquetas.csv'):
        if manifest.get(name)!=sha256(raiz/'datos/crudo'/name):
            errores.append(f'datos/crudo/{name}: cambió el archivo base; el supervisor debe revisar la extracción')
    raw_rows=leer_csv(raiz/'datos/crudo/calles_crudo.csv',['id','nombre_crudo','etiquetas','x_gk','y_gk','lat','lon','en_mapa'])
    raw={r['id']:r for r in raw_rows}
    if len(raw)!=len(raw_rows): errores.append('IDs repetidos en el inventario base')
    labels=leer_csv(raiz/'datos/crudo/etiquetas.csv',['handle','id_calle','nombre_crudo','x_gk','y_gk'])
    handles=[r['handle'].upper() for r in labels]
    if len(set(handles))!=len(handles): errores.append('Handles repetidos en etiquetas.csv')
    counts=Counter(r['id_calle'] for r in labels)
    for r in labels:
        if not re.fullmatch(r'[0-9A-Fa-f]+',r['handle']): errores.append('Handle inválido en etiquetas.csv')
        if r['id_calle'] not in raw or raw[r['id_calle']]['nombre_crudo']!=r['nombre_crudo']:
            errores.append(f"Handle {r['handle']}: no coincide con el inventario de calles")
    for key,r in raw.items():
        if str(counts[key])!=r['etiquetas']: errores.append(f'{key}: cantidad de rótulos inconsistente')
    rows={}
    for path in sorted((raiz/'datos/lotes').glob('lote-*.csv')):
        for line,r in enumerate(leer_csv(path,LOTE),2):
            where=f'{path.name}:{line} ({r["id"]})'
            def err(message): errores.append(f'{where}: {message}')
            if r['id'] not in raw: err('ID desconocido o con espacios'); continue
            if r['id'] in rows: err('ID repetido entre lotes')
            rows[r['id']]=dict(r,lote=path.name)
            if r['nombre_crudo']!=raw[r['id']]['nombre_crudo']: err('no modificar nombre_crudo')
            if any(v!=v.strip() for v in r.values()): err('quitar espacios al principio o final de los campos')
            if any(any(unicodedata.category(c).startswith('C') for c in v) for v in r.values()):
                err('no usar saltos de línea, tabuladores ni caracteres invisibles dentro de un campo')
            state=r['estado']
            if state not in ('','propuesta','en_consulta'):
                err('estado permitido: vacío, propuesta o en_consulta; aprobada se deriva de conformidad.csv')
            elif not state:
                if any(r[c] for c in ('nombre','tipo','homenaje','nota','fuente')): err('falta estado')
            elif state=='en_consulta':
                if r['nombre']: err('una consulta deja nombre vacío hasta resolver la duda')
                if not r['nota']: err('escribir la pregunta concreta en nota')
                if r['tipo'] and r['tipo'] not in TIPOS: err('tipo desconocido')
                if r['homenaje'] and r['homenaje'] not in HOMENAJES: err('homenaje desconocido')
            else:
                try: texto_cad(r['nombre'])
                except DatosInvalidos as e: err(str(e))
                if r['tipo'] not in TIPOS: err('tipo desconocido')
                if r['homenaje'] not in HOMENAJES: err('homenaje desconocido')
                if not r['fuente']: err('indicar fuente o criterio verificable; no inventar el homenaje')
                if r['nombre']!=r['nombre_crudo'] and not r['nota']: err('explicar la corrección en nota')
            if len(r['nota'])>500 or len(r['fuente'])>500: err('nota y fuente admiten hasta 500 caracteres cada una')
    if set(rows)!=set(raw): errores.append('los lotes deben contener exactamente los IDs del inventario base')
    approvals={}
    for a in leer_csv(raiz/'datos/conformidad.csv',CONFORMIDAD):
        key=a['id']
        if key in approvals: errores.append(f'Conformidad {key}: duplicada')
        approvals[key]=a; r=rows.get(key)
        if not r or r['estado']!='propuesta':
            errores.append(f'Conformidad {key}: requiere una propuesta existente'); continue
        if a['nombre_crudo']!=r['nombre_crudo'] or a['nombre_aprobado']!=r['nombre']:
            errores.append(f'Conformidad {key}: no corresponde al texto exacto de la propuesta actual')
        try:
            if date.fromisoformat(a['fecha']).isoformat()!=a['fecha']: raise ValueError()
        except ValueError: errores.append(f'Conformidad {key}: fecha requerida con formato AAAA-MM-DD')
        if not a['referencia'].strip(): errores.append(f'Conformidad {key}: falta referencia de la decisión municipal')
        if any(v!=v.strip() or any(unicodedata.category(c).startswith('C') for c in v) for v in a.values()):
            errores.append(f'Conformidad {key}: espacios extremos o caracteres de control')
    if errores: raise DatosInvalidos('\n'.join(errores))
    for key,r in rows.items(): r['estado_final']='aprobada' if key in approvals else r['estado'] or 'sin_revisar'
    return {'raw':raw,'labels':labels,'rows':rows,'approvals':approvals,
            'config':json.loads((raiz/'config/proyecto.json').read_text(encoding='utf-8'))}

def resumen(data):
    counts=Counter(r['estado_final'] for r in data['rows'].values())
    return {'total':len(data['rows']),'rotulos':len(data['labels']),
            **{k:counts[k] for k in ('sin_revisar','propuesta','en_consulta','aprobada')},
            'fuera_recorte':sum(r['en_mapa']!='si' for r in data['raw'].values())}

def inventario(data):
    return [dict(r,x_dibujo=data['raw'][key]['x_gk'],y_dibujo=data['raw'][key]['y_gk'],
                 dentro_recorte=data['raw'][key]['en_mapa']) for key,r in sorted(data['rows'].items())]

def geojson(data):
    return {'type':'FeatureCollection',
            'descripcion':'Inventario de puntos de referencia, no ejes de calles. Geometría nula hasta verificar CRS y correspondencia espacial.',
            'georreferenciacion_verificada':False,
            'features':[{'type':'Feature','id':r['id'],'geometry':None,'properties':r} for r in inventario(data)]}

def huellas(raiz=RAIZ):
    paths=sorted((Path(raiz)/'datos').rglob('*.csv'))+[Path(raiz)/'config/proyecto.json']
    return {str(p.relative_to(raiz)):sha256(p) for p in paths}
