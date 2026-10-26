"""La tarea del estudiante mantiene las exportaciones sin ocultar errores."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import codespaces
from comun import LOTE, escribir_csv, leer_csv


class ValidarTarea(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        for name in ('datos', 'config', 'web', 'scripts'):
            shutil.copytree(ROOT / name, self.root / name)

    def exportaciones(self):
        return {name: (self.root / 'web' / name).read_bytes()
                for name in ('datos.json', 'calles.csv', 'calles.geojson')}

    def editar(self, **fields):
        path = self.root / 'datos/lotes/lote-01.csv'
        rows = leer_csv(path)
        for row in rows:
            if row['id'] == '008':
                row.update(fields)
        escribir_csv(path, rows, LOTE)

    def test_validar_actualiza_las_tres_exportaciones_sin_cambiar_insumos(self):
        self.editar(nota='¿Qué documento respalda esta consulta de prueba?')
        before = self.exportaciones()
        inputs = {p: p.read_bytes() for name in ('datos', 'config')
                  for p in (self.root / name).rglob('*') if p.is_file()}
        with patch.object(codespaces, 'RAIZ', self.root):
            self.assertEqual(codespaces.ejecutar('validar'), 0)
        for name, content in self.exportaciones().items():
            self.assertNotEqual(content, before[name], name)
        data = json.loads((self.root / 'web/datos.json').read_text())
        row = next(r for r in data['calles'] if r['id'] == '008')
        self.assertEqual(row['nota'], '¿Qué documento respalda esta consulta de prueba?')
        self.assertEqual({p: p.read_bytes() for p in inputs}, inputs)

    def test_validacion_fallida_no_sobrescribe_exportaciones(self):
        self.editar(id='8')
        before = self.exportaciones()
        with patch.object(codespaces, 'RAIZ', self.root):
            self.assertNotEqual(codespaces.ejecutar('validar'), 0)
        self.assertEqual(self.exportaciones(), before)


if __name__ == '__main__':
    unittest.main()
