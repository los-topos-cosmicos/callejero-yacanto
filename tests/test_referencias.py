"""El contraste informa candidatos sin convertir similitudes en decisiones."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from auditar_referencias import clave, comparar, referencias


class Referencias(unittest.TestCase):
    def test_no_expande_iniciales_ni_fusiona_nombres_parecidos(self):
        for a,b in [('C. Velez','Juan C. Velez'),('Belgrano','Manuel Belgrano'),
                    ('Charcal','Charcas'),('Venecia','Venezia'),('Av. Virgen','Av. Virgen de la Merced')]:
            self.assertNotEqual(clave(a), clave(b))
    def test_busqueda_normalizada_no_equivale_a_nombre_oficial(self):
        self.assertEqual(clave('Av. Central'), clave('AV CENTRAL'))
        rows = comparar([{'id':'001','nombre_crudo':'Roque Sáenz Peña'}],
                        [{'codigo':'REF-1','nombre':'ROQUE SAENZ PENA','tipo':'CALLE','fuente':'TEST'}])
        self.assertEqual(rows[0]['comparacion'], 'candidato_por_texto')
        self.assertNotIn('estado', rows[0])
    def test_tramos_repetidos_no_duplican_candidato_y_ausencia_se_conserva(self):
        ref = {'codigo':'REF-1','nombre':'CENTRAL','tipo':'CALLE','fuente':'TEST'}
        rows = comparar([{'id':'001','nombre_crudo':'Central'},{'id':'002','nombre_crudo':'No encontrada'}], [ref,ref])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]['comparacion'], 'sin_coincidencia')
    def test_codigos_distintos_siguen_visibles(self):
        a = {'codigo':'REF-1','nombre':'CENTRAL','tipo':'CALLE','fuente':'TEST'}
        rows = comparar([{'id':'001','nombre_crudo':'Central'}], [a,dict(a,codigo='REF-2')])
        self.assertEqual({r['codigo_referencia'] for r in rows}, {'REF-1','REF-2'})
    def test_huellas_y_cobertura_de_instantaneas(self):
        refs = referencias()
        self.assertTrue(refs)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            shutil.copytree(ROOT/'datos/referencias',root/'datos/referencias')
            p=root/'datos/referencias/georef_villa_yacanto.json'
            p.write_text(p.read_text()+' ')
            with self.assertRaisesRegex(ValueError,'huella'):referencias(root)
