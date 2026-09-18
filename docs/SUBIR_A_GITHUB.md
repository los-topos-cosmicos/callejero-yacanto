# Subir a los-topos-cosmicos/callejero-yacanto

El repositorio de la captura ya existe y está vacío. No hace falta crear otro ni cargar un README desde la web. Esta guía prepara un primer commit local y lo sube; nadie ejecutó el push por vos en este paquete.

## Opción guiada: Terminal de macOS o Git Bash

Se necesita Git, Python 3.12+ y GitHub CLI (`gh`). Si falta `gh`, instalarlo desde [GitHub CLI](https://cli.github.com/). Descomprimir el ZIP y abrir Terminal dentro de la carpeta `callejero-yacanto`.

```bash
cd /ruta/a/callejero-yacanto
gh auth login --hostname github.com --git-protocol https --web
bash scripts/primer_push.sh --push
```

La primera línea se reemplaza por la ubicación real de la carpeta. El inicio de sesión lo hacés vos en GitHub. El script toma tu usuario autenticado para CODEOWNERS y configura un correo público `noreply` para ese repositorio; valida los datos, crea el commit y ejecuta `git push -u origin main`. No incluye credenciales en archivos ni ejecuta un push forzado.

El script solo acepta un remoto sin ramas. Si detecta contenido, otro `origin` o una rama local distinta de `main`, se detiene. Si una política de la organización rechaza el push, leer el error y pedir el acceso correspondiente; no desactivar reglas para eludirlo.

Antes de subir, completar lo que se conozca en `config/proyecto.json` y revisar la difusión de los datos con la autoridad. Los campos institucionales pendientes están señalados; no impiden que el código funcione.

## Comandos manuales equivalentes

Para revisar cada paso, usar estos comandos desde la carpeta descomprimida. Reemplazar `TU_USUARIO` y el correo por los de tu cuenta GitHub; se puede usar el `noreply` de Settings → Emails.

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
python3 scripts/configurar_responsable.py TU_USUARIO
python3 scripts/validar.py
git init -b main
git config user.name TU_USUARIO
git config user.email TU_CORREO_NOREPLY
git add .
git status --short
git commit -m "Preparar pasantía de callejero de dos meses"
git remote add origin https://github.com/los-topos-cosmicos/callejero-yacanto.git
git push -u origin main
```

Revisar `git status` antes del commit: no debe haber archivos ajenos al paquete. `.gitignore` excluye DWG/DXF y resultados temporales. No pegar una contraseña o token dentro de la URL del remoto.

## Si el remoto ya tiene contenido

No usar `--force`. Clonar el repositorio en otra carpeta, crear una rama, comparar el paquete con sus archivos y trasladar los cambios elegidos. Después, abrir un PR. No reemplazar a ciegas archivos de una versión ya trabajada.

```bash
git clone https://github.com/los-topos-cosmicos/callejero-yacanto.git callejero-trabajo
cd callejero-trabajo
git switch -c preparar-pasantia-dos-meses
# comparar y copiar aquí los archivos elegidos del paquete
# validar, revisar git diff, hacer commit y push de esta rama
```

## Después del primer push

1. En **Actions**, abrir `Validar callejero` y comprobar el resultado. Los documentos y el gráfico se descargan en Artifacts. El script local no demuestra que la ejecución remota haya pasado.
2. En **Settings → Rules → Rulesets**, crear una regla activa para `main`: exigir Pull Request, una aprobación, revisión de CODEOWNERS, descartar aprobaciones obsoletas y exigir el check `validar`. Ejecutar primero Actions para que el check aparezca como opción.
3. Bloquear force pushes y eliminación de `main`. El estudiante no debe tener Admin ni permiso de bypass. Los propietarios del código deben tener acceso Write; revisar que GitHub reconozca el usuario de `.github/CODEOWNERS`.
4. Añadir al estudiante con el acceso necesario y asignarle las primeras tareas de `ISSUES.md`. No publicar calificaciones ni datos personales innecesarios.
5. Si solo una persona puede revisar y ella misma propone cambios protegidos, designar un segundo revisor autorizado. No tratar la autoaprobación como revisión independiente.

Estas opciones las configura un administrador de la organización; no están activadas por existir el archivo CODEOWNERS. [Documentación de GitHub sobre propietarios y revisión requerida](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Publicar el visor es opcional

No se publica con el primer push. Si se acuerda su difusión: Settings → Pages → Source: GitHub Actions; crear la variable de repositorio `PUBLICAR_VISOR` con valor `true`; ejecutar manualmente el workflow `Publicar visor` sobre `main`. Solo se publica `web/`. Su aviso de georreferenciación pendiente permanece visible. Las aprobaciones y los procedimientos CAD no se alojan dentro de ese sitio, aunque los archivos versionados del repositorio público siguen siendo accesibles.

Fuentes de los comandos: [autenticación de GitHub CLI](https://cli.github.com/manual/gh_auth_login) y [primer push de un proyecto local](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).
