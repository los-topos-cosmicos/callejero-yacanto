#!/usr/bin/env python3
"""Informe de trabajo pendiente calculado desde los lotes y conformidades actuales."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
from comun import RAIZ, cargar, escribir_csv, huellas, resumen

TAREAS = {
    'sin_revisar': ('revisar_registro', 'Estudiante con supervisor', 'Revisar el registro y documentar una propuesta o una pregunta.'),
    'en_consulta': ('resolver_consulta', 'Supervisor / referente municipal', 'Obtener la evidencia solicitada y revisar la respuesta.'),
    'propuesta': ('revisar_propuesta', 'Supervisor / autoridad municipal', 'Revisar fuente y texto; registrar conformidad si la autoridad lo acepta.'),
}
ESTADOS = ('sin_revisar', 'en_consulta', 'propuesta', 'aprobada')


def recopilar(data):
    pendientes, espaciales, metadatos = [], [], []
    lotes = defaultdict(Counter)
    for key, row in sorted(data['rows'].items()):
        state = row['estado_final']
        lotes[row['lote']][state] += 1
        base = dict(id=key, lote=row['lote'], nombre_crudo=row['nombre_crudo'],
                    nombre_propuesto=row['nombre'], estado=state)
        if state in TAREAS:
            tarea, responsable, paso = TAREAS[state]
            pendientes.append(dict(base, tarea=tarea, responsable=responsable,
                                   detalle=row['nota'] or paso, siguiente_paso=paso, fuente=row['fuente']))
        if data['raw'][key]['en_mapa'] != 'si':
            espaciales.append(dict(base, siguiente_paso='Verificar ubicación y criterio del recorte con el plano original; no inferir geometría.'))
        faltan = [c for c in ('tipo', 'homenaje') if row[c] in ('', 'sin_confirmar')]
        if faltan and state != 'sin_revisar':
            metadatos.append(dict(base, campos_por_confirmar=', '.join(faltan)))
    por_lote = [dict(lote=lote, total=sum(counts.values()), **{s: counts[s] for s in ESTADOS})
                for lote, counts in sorted(lotes.items())]
    config = data['config']
    verificaciones = [
        dict(tema='Localidad del plano', estado='declarado_en_configuracion' if config['localidad_confirmada'] else 'pendiente',
             responsable='Supervisor / referente municipal', siguiente_paso='Conservar referencia institucional que vincule el DWG con la localidad.'),
        dict(tema='Sistema de coordenadas', estado='pendiente_verificacion_manual', responsable='Responsable SIG / agrimensor',
             siguiente_paso='Documentar CRS y controles del plano; el exportador mantiene geometrías nulas.'),
        dict(tema='Handles y textos del DWG', estado='pendiente_verificacion_manual', responsable='Operador CAD / supervisor',
             siguiente_paso='Cotejar entidades y textos contra una copia del DWG original.'),
        dict(tema='Prueba en AutoCAD', estado='declarado_en_configuracion' if config['prueba_autocad_en_copia'] else 'pendiente',
             responsable='Operador CAD', siguiente_paso='Completar o cotejar ACTA_PRUEBA_CAD.md; una declaración no es prueba generada por este informe.'),
    ]
    return dict(resumen=resumen(data), por_lote=por_lote, pendientes=pendientes,
                verificacion_espacial=espaciales, metadatos_por_confirmar=metadatos,
                verificaciones_proyecto=verificaciones)


def escribir(data, out, raiz=RAIZ):
    """Escribe en una carpeta de salida ya preparada por el generador llamante."""
    out = Path(out)
    report = recopilar(data)
    report['generado_utc'] = datetime.now(timezone.utc).isoformat()
    report['insumos_sha256'] = huellas(raiz)
    base = ['id','lote','nombre_crudo','nombre_propuesto','estado']
    escribir_csv(out/'pendientes_de_revision.csv', report['pendientes'],
                 base+['tarea','responsable','detalle','siguiente_paso','fuente'])
    escribir_csv(out/'resumen_por_lote.csv', report['por_lote'], ['lote','total',*ESTADOS])
    escribir_csv(out/'verificacion_espacial.csv', report['verificacion_espacial'], base+['siguiente_paso'])
    escribir_csv(out/'metadatos_por_confirmar.csv', report['metadatos_por_confirmar'], base+['campos_por_confirmar'])
    escribir_csv(out/'verificaciones_proyecto.csv', report['verificaciones_proyecto'],
                 ['tema','estado','responsable','siguiente_paso'])
    (out/'pendientes.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    s = report['resumen']
    lines = ['# Qué queda por hacer', '', f"Generado (UTC): {report['generado_utc']}", '',
             'Este informe refleja los archivos leídos, no el número de PRs abiertos o incorporados. '
             'Regenerarlo después de traer los cambios de main. Las huellas de los insumos están en pendientes.json.', '',
             f"Inventario: **{s['total']} registros**. Sin revisar: **{s['sin_revisar']}**; "
             f"consultas abiertas: **{s['en_consulta']}**; propuestas sin conformidad: **{s['propuesta']}**; "
             f"con conformidad registrada: **{s['aprobada']}**.", '',
             '**Incorporar un PR no resuelve automáticamente una consulta ni aprueba una propuesta.** '
             'Cada registro sin conformidad aparece una vez en pendientes_de_revision.csv, con ID, lote, '
             'pregunta o motivo, fuente, responsable por rol y siguiente paso.', '',
             '| Lote | Total | Sin revisar | Consultas | Propuestas sin conformidad | Con conformidad |',
             '|---|---:|---:|---:|---:|---:|']
    lines += [f"| {r['lote']} | {r['total']} | {r['sin_revisar']} | {r['en_consulta']} | {r['propuesta']} | {r['aprobada']} |"
              for r in report['por_lote']]
    lines += ['', '## Cómo usar la lista', '',
              '1. Filtrar pendientes_de_revision.csv por lote y tarea. Leer la pregunta completa y su fuente.',
              '2. Registrar la respuesta y la evidencia en la fila del lote. Si una consulta pasa a propuesta, '
              'seguirá pendiente de revisión y conformidad; no se considera cerrada por cambiar de estado.',
              '3. El supervisor registra conformidades reales sobre el texto exacto en datos/conformidad.csv. '
              'Regenerar el informe para ver la lista actualizada.', '',
              '## Verificaciones que siguen por separado', '',
              f"- verificacion_espacial.csv contiene **{len(report['verificacion_espacial'])}** registros fuera del recorte heredado. "
              'Pueden aparecer también en la lista de nombres; no se suman como calles adicionales.',
              f"- metadatos_por_confirmar.csv contiene **{len(report['metadatos_por_confirmar'])}** registros revisados con tipo u homenaje desconocido. "
              'Una conformidad sobre el nombre no certifica esos metadatos.',
              '- verificaciones_proyecto.csv separa localidad, CRS, correspondencia con el DWG y prueba CAD. '
              'Las declaraciones de configuración no se presentan como ensayos ejecutados por el informe.', '',
              'El lote 01 contiene material preparado para aprender: se incluye para no perder pendientes, '
              'pero no se atribuye como producción del estudiante. Las cantidades se calculan del estado actual.', '',
              'Puede haber cero registros sin revisar y seguir habiendo consultas, decisiones o controles técnicos pendientes. '
              'El informe no declara que el proyecto esté terminado por incorporar todos los PRs.']
    (out/'PENDIENTES.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return report


def generar(raiz, dest):
    raiz, dest = Path(raiz), Path(dest)
    data = cargar(raiz)
    if dest.exists():
        raise ValueError(f'{dest} ya existe. Elegir una carpeta nueva para conservar el informe anterior.')
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent, prefix='.pendientes-') as td:
        out = Path(td)
        escribir(data, out, raiz)
        out.rename(dest)
    return dest


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    ap.add_argument('--salida', type=Path, default=RAIZ/'build'/('pendientes-'+stamp))
    args = ap.parse_args()
    try:
        print(generar(RAIZ, args.salida)/'PENDIENTES.md')
    except (ValueError, OSError) as e:
        print(f'No se generó un informe nuevo: {e}', file=sys.stderr)
        sys.exit(1)
