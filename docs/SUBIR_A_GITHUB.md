# Trabajar y publicar desde GitHub

El repositorio `los-topos-cosmicos/callejero-yacanto` ya existe y está subido. La pasantía utiliza **GitHub Codespaces en el navegador**, con el entorno definido en el repositorio.

## Subir trabajo del estudiante

1. Abrir o reanudar su Codespace desde https://github.com/codespaces.
2. Crear una rama desde el nombre que aparece abajo a la izquierda.
3. Editar el lote y ejecutar **Terminal → Run Task → Callejero: Validar datos**.
4. En **Source Control**, revisar los cambios, elegir archivos con **+**, escribir un mensaje y pulsar **Commit**.
5. Pulsar **Publish Branch** la primera vez, o **Push / Sync Changes** después.
6. Abrir **Compare & pull request** en GitHub y completar la plantilla.

La [guía del estudiante](CODESPACES_ESTUDIANTE.md) explica cada clic. No hay `git init`, clonación ni configuración de credenciales en su computadora. Codespaces proporciona la autenticación de GitHub para el repositorio autorizado. [Documentación del flujo en el navegador](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace).

Antes de guardar un cambio de datos, el supervisor acompaña la regeneración de la copia exportada del visor: ejecutar `python3 scripts/construir.py` desde la terminal e incluir `web/datos.json`, `web/calles.csv` y `web/calles.geojson` en el mismo PR. La prueba `test_web_generada` reconstruye esos archivos en una carpeta temporal y exige que coincidan con los versionados; si falla, su mensaje indica cómo regenerarlos. No editar los archivos generados a mano.

## Proteger el trabajo

El supervisor configura una regla activa para `main`: exigir PR, una aprobación, revisión de CODEOWNERS, descartar aprobaciones obsoletas y exigir el check `validar`. Bloquear force pushes y eliminación de `main`; el estudiante no debe tener bypass. Los propietarios del código deben tener acceso Write y ser reconocidos por GitHub.

CODEOWNERS asigna responsables; la regla sobre `main` es la que exige su revisión. Si el propio responsable propone un cambio protegido, hace falta otro revisor autorizado. [Documentación de GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Publicar el visor en GitHub Pages

La captura del 18/09/2026 muestra **Deploy from a branch → main → /docs**. Esa selección publica las guías. Para publicar el visor previsto por este proyecto:

1. Abrir **Settings → Pages**.
2. En **Build and deployment → Source**, elegir **GitHub Actions**. El repositorio ya trae `publicar.yml`; no crear un workflow adicional desde las sugerencias.
3. Abrir **Settings → Secrets and variables → Actions → Variables**.
4. Crear la variable de repositorio **PUBLICAR_VISOR** con valor **true**, cuando se haya acordado la difusión.
5. Incorporar un PR a `main`: **Publicar visor** se ejecuta automáticamente. Para volver a publicar sin cambios, ir a **Actions → Publicar visor → Run workflow**, seleccionar `main` y ejecutar.
6. Esperar el resultado y abrir el enlace de despliegue. El destino previsto es https://los-topos-cosmicos.github.io/callejero-yacanto/.

El workflow valida los datos, audita las referencias y ejecuta todas las pruebas antes de reconstruir `web/` y publicar solo esa carpeta. Si alguna comprobación falla, el sitio conserva la versión publicada anteriormente. Antes de desplegar comprueba que el commit sigue siendo el actual de `main`; una ejecución antigua no publica sobre una versión posterior. La variable **PUBLICAR_VISOR** debe seguir en **true**; cambiarla desactiva las publicaciones siguientes.

Codespaces sirve una vista personal de trabajo en el puerto 8000; Pages publica la versión incorporada a `main` después de superar las comprobaciones. La edición del estudiante no necesita Pages para funcionar. Al recargar, el visor solicita `datos.json` sin reutilizar la caché del navegador. GitHub Pages puede tardar unos minutos en propagar un despliegue.

La configuración remota de Pages y la variable no se cambian por editar un archivo local del repositorio. [Fuente oficial sobre el origen de publicación](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Aplicar actualizaciones de configuración

El supervisor puede incorporar una actualización desde un Codespace, revisar los archivos y abrir un PR con las mismas herramientas. Tras integrar cambios en `.devcontainer/`, los espacios existentes usan **Codespaces: Rebuild Container**; los nuevos toman la configuración actual automáticamente.

No subir ZIPs como sustituto de los archivos del repositorio. Si se recibe un paquete de actualización, seguir su instrucción de aplicación y revisar el diff antes del commit; preservar los CSV de trabajo y `config/proyecto.json` existentes.
