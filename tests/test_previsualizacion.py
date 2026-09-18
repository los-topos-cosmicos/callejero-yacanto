"""El gráfico enseña qué cambió, no atribuye un lote entero al estudiante."""
from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from comun import cargar
from previsualizar import destacadas, cambios_desde_git, dibujar

class CambiosDelPR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=cargar();cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name)
        shutil.copytree(ROOT/'datos',cls.root/'datos')
        def git(*args):return subprocess.check_output(['git',*args],cwd=cls.root,stderr=subprocess.DEVNULL).decode().strip()
        git('init','-b','main');git('add','datos')
        git('-c','user.name=Prueba','-c','user.email=prueba@example.invalid','commit','-m','Base sintética')
        cls.base=git('rev-parse','HEAD')
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_seleccion_manual_acepta_rutas_y_no_mezcla_lotes(self):
        a=destacadas(self.data,['datos/lotes/lote-01.csv'])
        self.assertEqual(a,destacadas(self.data,['lote-01.csv']))
        self.assertEqual(len(a),10)
        self.assertFalse(a&destacadas(self.data,['lote-02.csv']))
    def test_datos_sin_cambios_no_resaltan_el_ejemplo(self):
        self.assertEqual(cambios_desde_git(self.data,self.base,self.root),set())
    def test_un_cambio_de_nota_resalta_una_sola_fila(self):
        data=deepcopy(self.data);data['rows']['008']['nota']='Confirmar con documentación municipal.'
        self.assertEqual(cambios_desde_git(data,self.base,self.root),{'008'})
    def test_reordenar_o_mover_una_fila_no_es_revisar_una_calle(self):
        data=deepcopy(self.data);data['rows']=dict(reversed(list(data['rows'].items())))
        data['rows']['008']['lote']='lote-02.csv'
        self.assertEqual(cambios_desde_git(data,self.base,self.root),set())
    def test_la_conformidad_cuenta_como_cambio_aunque_el_lote_no_cambie(self):
        data=deepcopy(self.data);data['approvals']['002']={'id':'002','referencia':'Ensayo'}
        self.assertEqual(cambios_desde_git(data,self.base,self.root),{'002'})
    def test_rechaza_una_base_que_no_es_sha(self):
        for base in ('main','--help','x; touch archivo','a'*39):
            with self.subTest(base=base),self.assertRaises(ValueError):cambios_desde_git(self.data,base,self.root)
    def test_grafico_conserva_la_interfaz_usada_por_los_informes(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/'general.png';b=Path(tmp)/'pr.png'
            dibujar(self.data,a);dibujar(self.data,b,ids={'008'})
            self.assertTrue(a.read_bytes().startswith(b'\x89PNG'))
            self.assertNotEqual(a.read_bytes(),b.read_bytes())

if __name__=='__main__':unittest.main()
