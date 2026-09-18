#!/usr/bin/env bash
# Ejecutar manualmente tras leer docs/SUBIR_A_GITHUB.md. Nunca usa --force.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "${1:-}" != "--push" ]]; then
  echo 'Uso: bash scripts/primer_push.sh --push'
  echo 'Prepara CODEOWNERS, hace el primer commit y lo sube al repositorio vacío indicado.'
  exit 0
fi
command -v git >/dev/null || { echo 'Falta Git.'; exit 1; }
command -v gh >/dev/null || { echo 'Falta GitHub CLI (gh). Ver instrucciones.'; exit 1; }
command -v python3 >/dev/null || { echo 'Falta Python 3.12 o posterior.'; exit 1; }
gh auth status
remote='https://github.com/los-topos-cosmicos/callejero-yacanto.git'
owner=$(gh api user --jq .login)
email=$(gh api user --jq '(.id|tostring) + "+" + .login + "@users.noreply.github.com"')
# Configura autenticación HTTPS de Git mediante la sesión de gh.
gh auth setup-git
refs=$(git ls-remote --heads "$remote")
if [[ -n "$refs" ]]; then
  echo 'El repositorio ya tiene ramas. Se detiene sin sobrescribirlas; ver la guía para repositorio con contenido.'
  exit 1
fi
if [[ -d .git ]]; then
  actual=$(git remote get-url origin 2>/dev/null || true)
  if [[ -n "$actual" && "$actual" != "$remote" ]]; then echo 'El remoto origin es distinto. No se modificó.'; exit 1; fi
  branch=$(git symbolic-ref --short HEAD)
  if [[ "$branch" != 'main' ]]; then echo 'Esta carpeta ya usa otra rama. Revisar manualmente.'; exit 1; fi
else
  git init -b main
fi
python3 scripts/configurar_responsable.py "$owner"
python3 scripts/validar.py
# Evitar archivos ajenos añadidos después de descomprimir, aunque no estén ignorados.
if find . -path './.git' -prune -o -path './.venv' -prune -o -type f \( -iname '*.dwg' -o -iname '*.dxf' \) -print | grep -q .; then
  echo 'Se detectó un DWG/DXF en la carpeta. Mantener los originales fuera del repositorio antes de continuar.'; exit 1
fi
git config user.name "$owner"
git config user.email "$email"
git add README.md EMPEZAR_AQUI.md CONTRIBUIR.md ISSUES.md LICENSE NOTICE.md PROCEDENCIA.md requirements.txt requirements-extraccion.txt .gitignore .github config datos docs entrega ejemplos propuesta scripts tests web
if ! git diff --cached --quiet; then git commit -m 'Preparar pasantía de callejero: dos meses y una hora por día hábil'; fi
if ! git remote get-url origin >/dev/null 2>&1; then git remote add origin "$remote"; fi
git push -u origin main
echo 'Subido. Activar las reglas de main y revisar la primera ejecución de Actions según la guía.'
