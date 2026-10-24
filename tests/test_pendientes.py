"""Los pendientes siguen a los datos: revisar o incorporar un PR no es aprobar."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from comun import cargar, escribir_csv, leer_csv, LOTE, CONFORMIDAD, DatosInvalidos, sha256
from generar_entrega import generar as generar_entrega
from pendientes import recopilar, generar


class Pendientes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)/'repo'
        for name in ('datos','config','docs','entrega'):
            shutil.copytree(ROOT/name, self.root/name)
        escribir_csv(self.root/'datos/conformidad.csv', [], CONFORMIDAD)

    def tearDown(self):
        self.tmp.cleanup()

    def update(self, key, **fields):
        for p in (self.root/'datos/lotes').glob('*.csv'):
            rows = leer_csv(p)
            if any(r['id'] == key for r in rows):
                for r in rows:
                    if r['id'] == key: r.update(fields)
                escribir_csv(p, rows, LOTE)
                return
        self.fail(key)

    def pending(self, key):
        return next((r for r in recopilar(cargar(self.root))['pendientes'] if r['id'] == key), None)

    def test_query_becomes_proposal_but_remains_until_exact_conformity(self):
        self.update('011', nombre='',tipo='',homenaje='',estado='en_consulta',
                    nota='¿Qué documento establece este nombre?',fuente='Fixture de consulta')
        self.assertEqual(self.pending('011')['tarea'], 'resolver_consulta')
        self.update('011', nombre='Arroyito',tipo='calle',homenaje='sin_confirmar',estado='propuesta',
                    nota='Conservación sintética para probar el flujo.',fuente='Fixture de propuesta')
        self.assertEqual(self.pending('011')['tarea'], 'revisar_propuesta')
        escribir_csv(self.root/'datos/conformidad.csv', [dict(id='011',nombre_crudo='Arroyito',
                     nombre_aprobado='Arroyito',fecha='2026-10-25',referencia='TEST-SINTETICO')], CONFORMIDAD)
        self.assertIsNone(self.pending('011'))
        report = recopilar(cargar(self.root))
        self.assertTrue(any(r['id']=='011' for r in report['metadatos_por_confirmar']))
        self.update('011',nombre='Arroyito Norte')
        with self.assertRaises(DatosInvalidos): generar(self.root, Path(self.tmp.name)/'obsoleto')

    def test_untouched_and_queried_rows_have_different_actions(self):
        self.update('011', **dict.fromkeys(LOTE[2:], ''))
        self.assertEqual(self.pending('011')['tarea'], 'revisar_registro')
        self.update('011',estado='en_consulta',nota='¿Qué fuente falta?')
        self.assertEqual(self.pending('011')['detalle'], '¿Qué fuente falta?')
        self.assertEqual(self.pending('011')['tarea'], 'resolver_consulta')

    def test_spatial_work_overlaps_names_without_duplicating_pending_rows(self):
        data = cargar(self.root)
        report = recopilar(data)
        self.assertEqual(len(report['verificacion_espacial']), report['resumen']['fuera_recorte'])
        self.assertEqual(len({r['id'] for r in report['pendientes']}), len(report['pendientes']))
        self.assertEqual(len(report['pendientes'])+report['resumen']['aprobada'], report['resumen']['total'])
        self.assertTrue({r['id'] for r in report['verificacion_espacial']} <= {r['id'] for r in report['pendientes']})
        for state in ('sin_revisar','en_consulta','propuesta','aprobada'):
            self.assertEqual(sum(r[state] for r in report['por_lote']), report['resumen'][state])

    def test_new_report_keeps_exact_questions_sources_and_input_hashes(self):
        question = '¿Qué documento, versión y apartado confirman este nombre?'
        self.update('011',nombre='',tipo='',homenaje='',estado='en_consulta',nota=question,fuente='TEST: expediente pendiente')
        out = generar(self.root, Path(self.tmp.name)/'informe')
        rows = leer_csv(out/'pendientes_de_revision.csv')
        row = next(r for r in rows if r['id']=='011')
        self.assertEqual(row['detalle'], question)
        self.assertEqual(row['fuente'], 'TEST: expediente pendiente')
        report = json.loads((out/'pendientes.json').read_text())
        key = 'datos/lotes/lote-02.csv'
        self.assertEqual(report['insumos_sha256'][key], sha256(self.root/key))
        self.assertIn('Incorporar un PR no resuelve', (out/'PENDIENTES.md').read_text())
        with self.assertRaisesRegex(ValueError, 'ya existe'): generar(self.root, out)

    def test_invalid_data_cannot_create_a_new_or_replace_an_existing_report(self):
        out = generar(self.root, Path(self.tmp.name)/'informe')
        previous = (out/'pendientes.json').read_bytes()
        self.update('011', **dict.fromkeys(LOTE[2:], ''))
        self.update('011',estado='en_consulta',nombre='Nombre inventado',nota='¿Cuál es la evidencia?')
        new = Path(self.tmp.name)/'informe-nuevo'
        with self.assertRaises(DatosInvalidos): generar(self.root, new)
        self.assertFalse(new.exists())
        with self.assertRaises(DatosInvalidos): generar(self.root, out)
        self.assertEqual((out/'pendientes.json').read_bytes(), previous)

    def test_delivery_includes_the_same_report_and_hashes_every_output(self):
        out = generar_entrega(self.root, Path(self.tmp.name)/'entrega', con_pdf=False)
        report = json.loads((out/'pendientes.json').read_text())
        manifest = json.loads((out/'manifest.json').read_text())
        self.assertEqual(report['resumen'], manifest['resumen'])
        for name in ('PENDIENTES.md','pendientes_de_revision.csv','resumen_por_lote.csv',
                     'verificacion_espacial.csv','verificaciones_proyecto.csv','metadatos_por_confirmar.csv','pendientes.json'):
            self.assertEqual(manifest['salidas_sha256'][name], sha256(out/name))
