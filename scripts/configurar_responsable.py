#!/usr/bin/env python3
"""Registra el usuario que revisará archivos protegidos; no configura permisos remotos."""
import argparse
import re
from comun import RAIZ
ap=argparse.ArgumentParser(); ap.add_argument('usuario',help='Usuario real de GitHub, sin @')
a=ap.parse_args()
if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',a.usuario): ap.error('Usuario de GitHub inválido')
paths=['/datos/crudo/','/datos/conformidad.csv','/scripts/','/tests/','/entrega/','/.github/','/.devcontainer/','/.vscode/','/config/','/requirements*.txt','/web/index.html']
text='# Requiere usuario con acceso Write y reglas sobre main que exijan revisión de CODEOWNERS.\n'
text+=''.join(f'{path} @{a.usuario}\n' for path in paths)
(RAIZ/'.github/CODEOWNERS').write_text(text,encoding='utf-8')
print('Responsable configurado. Activar las reglas según docs/SUBIR_A_GITHUB.md.')
