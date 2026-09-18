#!/usr/bin/env bash
# Se ejecuta automáticamente EN GITHUB, nunca en la computadora del estudiante.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt -r requirements-extraccion.txt
# Un CSV a medio editar no debe impedir reabrir el entorno para corregirlo.
if .venv/bin/python scripts/validar.py; then
  echo 'Entorno listo. Abrir docs/CODESPACES_ESTUDIANTE.md.'
else
  echo 'Entorno instalado. Hay datos por corregir; ver los mensajes de validación.'
fi
