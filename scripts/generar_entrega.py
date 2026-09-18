#!/usr/bin/env python3
"""Genera un paquete nuevo desde una única lectura validada de los datos."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from comun import RAIZ, LOTE, cargar, resumen, inventario, escribir_csv, geojson, texto_cad, huellas, sha256

def cambios(data,solo_aprobadas):
    result=[]
    for label in data['labels']:
        r=data['rows'][label['id_calle']]
        if r['estado']!='propuesta' or r['nombre']==r['nombre_crudo']: continue
        if solo_aprobadas and r['estado_final']!='aprobada': continue
        texto_cad(label['nombre_crudo']); texto_cad(r['nombre'])
        result.append({'handle':label['handle'],'id':r['id'],'texto_actual':label['nombre_crudo'],
                       'texto_nuevo':r['nombre'],'estado':r['estado_final']})
    return result

def archivo_cad(path,rows,mode,encoding='utf-8'):
    content=f'# CALLEJERO|1|{mode}\n# handle|texto_actual|texto_nuevo\n'
    content+=''.join(f"{r['handle']}|{r['texto_actual']}|{r['texto_nuevo']}\n" for r in rows)
    # Toda la conversión sucede antes de escribir. Nunca sustituir caracteres.
    path.write_bytes(content.replace('\n','\r\n').encode(encoding,errors='strict'))

def informe(data,out):
    from reportlab.platypus import Image, PageBreak
    from pdf_util import build,p,h,kicker,table
    from previsualizar import dibujar
    s=resumen(data); approved=cambios(data,True); proposed=cambios(data,False)
    changed={r['id'] for r in proposed}; touched=[r for r in inventario(data) if r['estado']]
    dibujar(data,out/'avance.png')
    story=[kicker('Informe de revisión · sin efecto oficial automático'),
           p('Callejero municipal\nEstado de la propuesta','TitleC'),
           p('Este informe refleja los archivos del paquete que lo acompaña. No acredita ejecución en AutoCAD ni aceptación municipal.'),
           table(['Indicador','Cantidad'],[['Calles en el inventario',s['total']],['Rótulos asociados',s['rotulos']],
             ['Propuestas sin conformidad',s['propuesta']],['Consultas abiertas',s['en_consulta']],
             ['Con conformidad registrada',s['aprobada']],['Sin revisar',s['sin_revisar']],
             ['Calles con cambio de grafía propuesto',len(changed)],['Rótulos en archivo CAD aprobado',len(approved)]],[355,148]),
           h('Cómo leer los resultados'),
           p('El lote 01 es un ejemplo preparado: 6 propuestas de conservar el rótulo y 4 consultas. No representa trabajo ya realizado por el estudiante. Una conformidad valida el nombre exacto registrado, no las hipótesis biográficas ni las coordenadas.'),
           p('actualizaciones_aprobadas_utf8.txt contiene solo cambios de nombre con conformidad. propuestas_simulacion_utf8.txt permite revisar todas las propuestas y la rutina bloquea su aplicación.'),
           p('El manifiesto incluye las huellas SHA-256 de insumos y salidas. La documentación institucional respaldatoria se conserva fuera del repositorio público.'),
           PageBreak(),kicker('Avance y alcance espacial'),h('Todas las calles cuentan'),
           Image(str(out/'avance.png'),width=503,height=268.3),
           p(f"Las {s['fuera_recorte']} calles fuera del recorte heredado siguen en el inventario. Su causa y ubicación deben comprobarse; no se presume que pertenezcan a láminas de detalle."),
           h('Limitaciones pendientes'),
           table(['Tema','Estado'],[['Localidad','Pendiente de confirmación municipal. El nombre del repositorio no es evidencia geográfica.'],
             ['Sistema de coordenadas','No verificado. El GeoJSON conserva atributos con geometría nula.'],
             ['Handles y textos','Consistencia de CSV verificada. Correspondencia con el DWG original pendiente de prueba en copia.'],
             ['AutoLISP','Revisión estática y pruebas de generadores; no ejecutado en AutoCAD.']],[125,378]),
           PageBreak(),kicker('Trabajo documentado'),h('Consultas para la autoridad')]
    queries=[r for r in touched if r['estado']=='en_consulta']
    story.append(table(['ID / rótulo','Pregunta'],[[r['id']+' / '+r['nombre_crudo'],r['nota']] for r in queries] or [['—','No hay consultas.']],[145,358]))
    story.extend([h('Propuestas registradas'),table(['ID / antes','Después / estado'],
        [[r['id']+' / '+r['nombre_crudo'],r['nombre']+' / '+r['estado_final']] for r in touched if r['estado']=='propuesta'] or [['—','No hay propuestas.']],[230,273]),
        p('El archivo inventario_completo.csv incluye las 251 filas, notas y fuentes completas. consultas_pendientes.csv contiene las preguntas sin truncar. La firma del informe por sí sola no carga conformidades: el supervisor registra los nombres aceptados en datos/conformidad.csv y regenera el paquete.'),
        h('Recepción y decisión'),p('Fecha: __________________  Referencia interna: __________________\nAutoridad / cargo: __________________________________________\nDecisión: recibido / requiere ajustes / conformidad de nombres adjunta\nFirma: ___________________________________________________')])
    build(out/'informe_de_cambios.pdf',story,'Informe de revisión')

def generar(raiz,dest,con_pdf=True):
    raiz=Path(raiz); dest=Path(dest)
    data=cargar(raiz)  # Abort before opening output files if any input is invalid.
    approved=cambios(data,True); proposals=cambios(data,False)
    if dest.exists(): raise ValueError(f'{dest} ya existe. Elegir una carpeta nueva para conservar la entrega anterior.')
    dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent,prefix='.entrega-') as td:
        out=Path(td)
        archivo_cad(out/'actualizaciones_aprobadas_utf8.txt',approved,'APROBADAS')
        archivo_cad(out/'propuestas_simulacion_utf8.txt',proposals,'SIMULACION')
        # Auxiliar para inspección/importación externa; la rutina suministrada usa UTF-8 explícito.
        archivo_cad(out/'actualizaciones_aprobadas_cp1252.txt',approved,'AUXILIAR_CP1252','cp1252')
        fields=['handle','id','texto_actual','texto_nuevo','estado']
        escribir_csv(out/'actualizaciones_aprobadas.csv',approved,fields)
        escribir_csv(out/'propuestas_por_rotulo.csv',proposals,fields)
        escribir_csv(out/'inventario_completo.csv',inventario(data),LOTE+['estado_final','lote','x_dibujo','y_dibujo','dentro_recorte'])
        escribir_csv(out/'consultas_pendientes.csv',[r for r in data['rows'].values() if r['estado']=='en_consulta'],LOTE)
        (out/'callejero.geojson').write_text(json.dumps(geojson(data),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        shutil.copy2(raiz/'entrega/actualizar_calles.lsp',out)
        shutil.copy2(raiz/'entrega/INSTRUCCIONES.md',out)
        shutil.copy2(raiz/'docs/ACTA_PRUEBA_CAD.md',out)
        if con_pdf: informe(data,out)
        manifest={'resumen':resumen(data),'insumos_sha256':huellas(raiz),'dwg_sha256_declarado':data['config']['dwg_sha256'],
                  'autocad_ejecutado_por_generador':False,'georreferenciacion_verificada':False,
                  'salidas_sha256':{p.name:sha256(p) for p in sorted(out.iterdir()) if p.is_file()}}
        (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        out.rename(dest)
    return dest

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--salida',type=Path,default=RAIZ/'build/entrega')
    args=ap.parse_args(); print(generar(RAIZ,args.salida))
