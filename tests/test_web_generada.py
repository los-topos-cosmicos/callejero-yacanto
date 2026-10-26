"""La copia exportada del visor debe corresponder a los datos actuales."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from comun import cargar
from construir import construir


class WebGenerada(unittest.TestCase):
    def test_exportaciones_versionadas_coinciden_con_los_lotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            construir(cargar(ROOT), out)
            for name in ('datos.json', 'calles.csv', 'calles.geojson'):
                with self.subTest(archivo=name):
                    self.assertEqual(
                        (ROOT / 'web' / name).read_bytes(),
                        (out / name).read_bytes(),
                        f'web/{name} está desactualizado. Ejecutar '
                        'python3 scripts/construir.py e incluir los tres '
                        'archivos generados de web/ en el mismo PR.',
                    )


if __name__ == '__main__':
    unittest.main()
