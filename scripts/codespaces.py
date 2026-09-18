#!/usr/bin/env python3
"""Acciones del menú Tasks; todas se ejecutan dentro del Codespace."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen
from comun import RAIZ, cargar

ACTIONS=('validar','vista','pruebas','entrega','propuesta','iniciar')

def disponible():
    try:
        with urlopen('http://127.0.0.1:8000/__callejero_ready',timeout=.5) as response:
            return json.load(response).get('aplicacion')=='callejero'
    except (URLError,ValueError,OSError):return False

def iniciar():
    if disponible():
        print('Visor ya iniciado. Abrir Ports / Puertos → 8000 → Open in Browser.');return
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',8000))==0:
            raise RuntimeError('El puerto 8000 está ocupado por otro servicio. Consultar al supervisor.')
    out=RAIZ/'build/codespaces';out.mkdir(parents=True,exist_ok=True)
    with (out/'visor.log').open('a',encoding='utf-8') as log:
        proc=subprocess.Popen([sys.executable,str(RAIZ/'scripts/servir.py')],cwd=RAIZ,
                              stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
    for _ in range(30):
        if disponible():
            print('Visor listo. Abrir Ports / Puertos → 8000 → Open in Browser.');return
        if proc.poll() is not None:break
        time.sleep(.1)
    raise RuntimeError('El visor no inició. El supervisor puede revisar build/codespaces/visor.log.')

def ejecutar(action):
    if action=='validar':return subprocess.call([sys.executable,'scripts/validar.py'],cwd=RAIZ)
    if action=='pruebas':return subprocess.call([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=RAIZ)
    if action=='propuesta':return subprocess.call([sys.executable,'scripts/generar_propuesta.py'],cwd=RAIZ)
    if action=='vista':
        from servir import actualizar
        from previsualizar import dibujar
        actualizar();dibujar(cargar(),RAIZ/'build/avance.png')
        print('Vista actualizada; recargar la pestaña del puerto 8000. Gráfico: build/avance.png')
    elif action=='entrega':
        from generar_entrega import generar
        stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
        dest=generar(RAIZ,RAIZ/'build'/('entrega-'+stamp))
        print(f'Entrega generada: {dest.relative_to(RAIZ)}\nAbrir archivos desde Explorer; Download si hay que compartirlos.')
    elif action=='iniciar':iniciar()
    else:raise ValueError(f'Acción desconocida: {action}')
    return 0

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('accion',choices=ACTIONS)
    args=ap.parse_args()
    try:sys.exit(ejecutar(args.accion))
    except (ValueError,OSError,RuntimeError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
