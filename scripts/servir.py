#!/usr/bin/env python3
"""Vista del Codespace: valida al recargar y solo sirve una carpeta de salidas."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import threading
from urllib.parse import urlsplit
from comun import RAIZ, DatosInvalidos, cargar
from construir import construir

READY = '/__callejero_ready'
LOCK = threading.Lock()

def actualizar(raiz=RAIZ):
    raiz=Path(raiz)
    data=cargar(raiz)
    out=raiz/'build/visor'
    construir(data,out)
    shutil.copy2(raiz/'web/index.html',out/'index.html')
    return out

class Visor(SimpleHTTPRequestHandler):
    def __init__(self,*args,raiz=RAIZ,**kwargs):
        self.raiz=Path(raiz)
        super().__init__(*args,directory=str(self.raiz/'build/visor'),**kwargs)

    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        super().end_headers()

    def do_GET(self):
        path=urlsplit(self.path).path
        if path==READY:
            content=b'{"aplicacion":"callejero","version":1}'
            self.send_response(200);self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
            return
        # Serializar reconstrucción y lectura: no servir mezclas de dos versiones.
        with LOCK:
            try:
                actualizar(self.raiz)
            except (DatosInvalidos,ValueError,OSError) as e:
                content=('Hay datos por corregir. No se muestra una vista anterior como si fuera actual.\n\n'
                         +str(e)+'\n\nCorregir el CSV, guardar y recargar esta página.').encode('utf-8')
                self.send_response(503);self.send_header('Content-Type','text/plain; charset=utf-8')
                self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
                return
            super().do_GET()

    def do_HEAD(self):
        self.send_error(405,'Usar GET')

    def list_directory(self,path):
        self.send_error(403,'Listado de directorios desactivado')
        return None

def servidor(raiz=RAIZ,port=8000,host='0.0.0.0'):
    return ThreadingHTTPServer((host,port),partial(Visor,raiz=raiz))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--puerto',type=int,default=8000)
    args=ap.parse_args()
    with servidor(port=args.puerto) as http:
        print(f'Visor iniciado en puerto {args.puerto}. Abrir desde Ports / Puertos.',flush=True)
        http.serve_forever()
