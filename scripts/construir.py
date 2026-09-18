#!/usr/bin/env python3
import json
from comun import RAIZ, LOTE, cargar, inventario, escribir_csv, geojson, resumen

def construir(data,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/'calles.geojson').write_text(json.dumps(geojson(data),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'datos.json').write_text(json.dumps({'resumen':resumen(data),'calles':inventario(data)},ensure_ascii=False)+'\n',encoding='utf-8')
    escribir_csv(out/'calles.csv',inventario(data),LOTE+['estado_final','lote','x_dibujo','y_dibujo','dentro_recorte'])

if __name__=='__main__':
    construir(cargar(),RAIZ/'web')
    print('web/: inventario actualizado; geometrías geográficas pendientes de verificación.')
