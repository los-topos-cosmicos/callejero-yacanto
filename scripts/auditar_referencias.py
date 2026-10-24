#!/usr/bin/env python3
"""Compara nombres con referencias nacionales sin editar lotes ni inferir geometrías."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import unicodedata
from comun import RAIZ, cargar, escribir_csv, sha256


def clave(texto):
    # INDEC documenta búsqueda sin tildes/ñ. Esta clave solo busca candidatos:
    # no prueba identidad, no expande iniciales ni elimina artículos o títulos.
    texto = unicodedata.normalize('NFKD', texto).casefold()
    palabras = re.findall(r'[a-z0-9]+', ''.join(c for c in texto if not unicodedata.combining(c)))
    if palabras and palabras[0] == 'avenida':
        palabras[0] = 'av'
    elif palabras and palabras[0] == 'pasaje':
        palabras[0] = 'pje'
    return ' '.join(palabras)


def referencias(raiz=RAIZ):
    carpeta = Path(raiz) / 'datos/referencias'
    fuentes = json.loads((carpeta/'fuentes.json').read_text(encoding='utf-8'))['fuentes']
    por_id = {f['id']: f for f in fuentes}
    for fuente in fuentes:
        if 'archivo' in fuente and sha256(carpeta/fuente['archivo']) != fuente['sha256']:
            raise ValueError(f"Referencia {fuente['id']}: cambió la instantánea; revisar fuente y huella")
    georef = json.loads((carpeta/por_id['GEOREF-VY']['archivo']).read_text(encoding='utf-8'))
    indec = json.loads((carpeta/por_id['INDEC2022-VY']['archivo']).read_text(encoding='utf-8'))
    if len(georef['calles']) != georef['total'] or georef['inicio'] != 0:
        raise ValueError('Georef: respuesta incompleta o paginada')
    if len(indec['features']) != indec['numberMatched'] or indec['numberReturned'] != indec['numberMatched']:
        raise ValueError('INDEC: respuesta incompleta o paginada')
    result = []
    for r in georef['calles']:
        if r['localidad_censal']['id'] != '14007360' or r['departamento']['id'] != '14007':
            raise ValueError('Georef: localidad ajena a Villa Yacanto')
        result.append(dict(codigo=r['id'], nombre=r['nombre'], tipo=r['categoria'], fuente='GEOREF-VY'))
    for feature in indec['features']:
        r = feature['properties']
        if r['clc'] != '14007360' or r['cde'] != '14007' or r['cpr'] != '14':
            raise ValueError('INDEC: localidad ajena a Villa Yacanto')
        if feature.get('geometry') is not None:
            raise ValueError('La instantánea de contraste debe contener solo atributos')
        result.append(dict(codigo=r['cod_indec'], nombre=r['fna'], tipo=r['subtipo'], fuente='INDEC2022-VY'))
    return result


def comparar(filas, refs):
    indice = defaultdict(list)
    for r in refs:
        indice[clave(r['nombre'])].append(r)
    result = []
    for fila in filas:
        candidatos = defaultdict(set)
        for r in indice.get(clave(fila['nombre_crudo']), []):
            # Un mismo código aparece en distintos tramos; no son calles nuevas.
            candidatos[(r['codigo'], r['nombre'], r['tipo'])].add(r['fuente'])
        if not candidatos:
            result.append(dict(id=fila['id'], nombre_crudo=fila['nombre_crudo'], codigo_referencia='',
                               nombre_referencia='', tipo_referencia='', fuentes='', comparacion='sin_coincidencia'))
        for (codigo, nombre, tipo), fuentes in sorted(candidatos.items()):
            result.append(dict(id=fila['id'], nombre_crudo=fila['nombre_crudo'], codigo_referencia=codigo,
                               nombre_referencia=nombre, tipo_referencia=tipo, fuentes='; '.join(sorted(fuentes)),
                               comparacion='candidato_por_texto'))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--salida', type=Path, default=RAIZ/'build/cruce_referencias.csv')
    args = ap.parse_args()
    data = cargar()
    rows = comparar(data['rows'].values(), referencias())
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    escribir_csv(args.salida, rows, ['id','nombre_crudo','codigo_referencia','nombre_referencia',
                                   'tipo_referencia','fuentes','comparacion'])
    ids = {r['id'] for r in rows if r['codigo_referencia']}
    print(f'{len(ids)} registros con candidatos de texto de {len(data["rows"])}. '
          'No es identidad espacial ni conformidad municipal. ' + str(args.salida))


if __name__ == '__main__':
    main()
