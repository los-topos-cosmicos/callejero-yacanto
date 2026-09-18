"""Pruebas de integración de la vista que se ejecutará dentro de Codespaces."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from comun import leer_csv, escribir_csv, LOTE
from servir import Visor
from codespaces import ACTIONS

class VistaCodespaces(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        for name in ('datos','config','web'):shutil.copytree(ROOT/name,self.root/name)
        self.original=(self.root/'web/datos.json').read_bytes()
        self.http=ThreadingHTTPServer(('127.0.0.1',0),partial(Visor,raiz=self.root))
        self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
        self.base=f'http://127.0.0.1:{self.http.server_port}'
    def tearDown(self):
        self.http.shutdown();self.thread.join();self.http.server_close();self.tmp.cleanup()
    def get(self,path):
        with urlopen(self.base+path,timeout=3) as response:
            return response.status,response.headers,response.read()
    def edit(self,**fields):
        path=self.root/'datos/lotes/lote-01.csv';rows=leer_csv(path)
        for row in rows:
            if row['id']=='008':row.update(fields)
        escribir_csv(path,rows,LOTE)
    def test_health_and_valid_preview(self):
        status,headers,body=self.get('/__callejero_ready')
        self.assertEqual(json.loads(body)['aplicacion'],'callejero')
        status,headers,body=self.get('/datos.json')
        self.assertEqual(status,200);self.assertEqual(len(json.loads(body)['calles']),251)
        self.assertEqual(headers['Cache-Control'],'no-store')
        self.assertEqual((self.root/'web/datos.json').read_bytes(),self.original)
    def test_saving_a_csv_is_reflected_on_reload(self):
        self.get('/datos.json');self.edit(nota='Consulta actualizada desde el navegador')
        data=json.loads(self.get('/datos.json')[2])
        self.assertEqual(next(r for r in data['calles'] if r['id']=='008')['nota'],'Consulta actualizada desde el navegador')
    def test_invalid_data_does_not_serve_stale_preview_and_recovers(self):
        self.get('/datos.json');self.edit(nombre='Nombre inventado')
        with self.assertRaises(HTTPError) as captured:self.get('/datos.json')
        self.assertEqual(captured.exception.code,503)
        self.assertIn('nombre vacío',captured.exception.read().decode())
        self.edit(nombre='')
        self.assertEqual(self.get('/datos.json')[0],200)
    def test_only_generated_web_directory_is_served(self):
        for path in ('/config/proyecto.json','/datos/crudo/etiquetas.csv','/../../config/proyecto.json'):
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as captured:self.get(path)
                self.assertEqual(captured.exception.code,404)
    def test_tasks_and_lifecycle_point_to_real_commands(self):
        cfg=json.loads((ROOT/'.devcontainer/devcontainer.json').read_text())
        tasks=json.loads((ROOT/'.vscode/tasks.json').read_text())['tasks']
        self.assertEqual(cfg['forwardPorts'],[8000])
        self.assertEqual(cfg['waitFor'],'postCreateCommand')
        self.assertTrue((ROOT/'.devcontainer/preparar.sh').exists())
        for filename in cfg['customizations']['codespaces']['openFiles']:
            self.assertTrue((ROOT/filename).is_file())
        self.assertEqual({t['args'][1] for t in tasks},set(ACTIONS))
        for task in tasks:self.assertTrue((ROOT/task['args'][0]).is_file())

if __name__=='__main__':unittest.main()
