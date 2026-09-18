#!/usr/bin/env python3
"""Audita TEXT/MTEXT del DXF sin sobrescribir inventario, lotes ni aprobaciones."""
import argparse
import json
import platform
from pathlib import Path
from comun import RAIZ, escribir_csv, leer_csv, sha256

def extraer(dxf_path,out,dwg_path=None):
    import ezdxf
    if out.exists() and any(out.iterdir()): raise ValueError('La carpeta de salida debe estar vacía o no existir.')
    doc=ezdxf.readfile(dxf_path)
    previous={r['handle'].upper():r for r in leer_csv(RAIZ/'datos/crudo/etiquetas.csv')}
    rows=[]; seen=set()
    # Todas las disposiciones se auditan; solo modelo puede ser elegible para CAD.
    for layout in doc.layouts:
        for entity in layout:
            if entity.dxftype() not in ('TEXT','MTEXT') or entity.dxf.layer!='NOMBRE CALLES': continue
            handle=entity.dxf.handle.upper()
            if handle in seen: raise ValueError(f'Handle duplicado: {handle}')
            seen.add(handle)
            original=entity.text if entity.dxftype()=='MTEXT' else entity.dxf.text
            plain=entity.plain_text()
            old=previous.get(handle)
            rows.append({'handle':handle,'tipo':entity.dxftype(),'espacio':layout.name,
                         'texto_original':original,'texto_plano':plain,
                         'x':entity.dxf.insert.x,'y':entity.dxf.insert.y,
                         'id_previo':old['id_calle'] if old else '',
                         'coincidencia_previa':'si' if old and old['nombre_crudo']==plain else 'no'})
    rows.sort(key=lambda r:int(r['handle'],16))
    if not rows: raise ValueError('No se encontraron rótulos TEXT/MTEXT en la capa NOMBRE CALLES.')
    out.mkdir(parents=True,exist_ok=True)
    escribir_csv(out/'rotulos_extraidos.csv',rows,list(rows[0]))
    metadata={'dxf_sha256':sha256(dxf_path),'dwg_sha256':sha256(dwg_path) if dwg_path else None,
              'python':platform.python_version(),'ezdxf':ezdxf.__version__,
              'rotulos':len(rows),'handles_unicos':len(seen),
              'sin_coincidencia_previa':sum(r['coincidencia_previa']!='si' for r in rows),
              'handles_previos_ausentes':sorted(set(previous)-seen),
              'crs_verificado':False,'conversion_dwg_dxf_verificada':False,
              'alcance':'Entidades directas TEXT/MTEXT en layouts; no expande bloques ni reescribe la base. No infiere coordenadas geográficas.'}
    (out/'procedencia.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return metadata

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('dxf',type=Path)
    ap.add_argument('--dwg',type=Path); ap.add_argument('--salida',type=Path,default=RAIZ/'build/extraccion')
    args=ap.parse_args(); print(json.dumps(extraer(args.dxf,args.salida,args.dwg),indent=2))
