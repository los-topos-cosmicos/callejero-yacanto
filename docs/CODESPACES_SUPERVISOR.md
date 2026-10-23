# Preparar una pasantía sin configuración local

El estudiante necesita su cuenta GitHub, navegador e internet. El supervisor prepara acceso, disponibilidad del servicio y revisión de trabajo; el repositorio automatiza Python, dependencias, editor y visor en Codespaces.

## Antes de la primera sesión

1. Dar al estudiante acceso **Write** al repositorio y exigir PR sobre `main`, con el check `validar` y revisión del supervisor. Así puede publicar ramas de trabajo sin configurar un fork. No necesita acceso Admin.
2. Confirmar que su cuenta puede crear un Codespace de este repositorio. El servicio puede usar una cuota personal o facturación habilitada por una organización elegible; definir esto antes de la sesión. No prometer disponibilidad gratuita ilimitada.
3. Usar una máquina de **2 núcleos**. `hostRequirements.cpus=2` solicita un mínimo, no impone un máximo: si la organización paga, restringir tamaños mediante su política de Codespaces cuando esté disponible.
4. Definir un tiempo de inactividad breve, por ejemplo 15 minutos, en las opciones de la cuenta o en la política de la organización. Al cerrar una sesión, enseñar a detener el espacio; la retención de un espacio detenido puede seguir consumiendo almacenamiento.
5. Abrir un Codespace nuevo de la rama con esta configuración y realizar la prueba de aceptación siguiente. Si se usa un espacio creado antes del cambio, ejecutar **Codespaces: Rebuild Container** desde la paleta para aplicar el entorno.
6. Revisar la configuración de Pages por separado si se desea publicar el visor. Ver `SUBIR_A_GITHUB.md`.

La organización puede asumir el consumo según su plan y configuración; no se cambió la facturación mediante este repositorio. Referencia: [gestión del costo de Codespaces](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-the-cost-of-github-codespaces-in-your-organization).

## Qué prepara automáticamente

| Elemento | Archivo que lo define |
|---|---|
| Python 3.12, usuario y GitHub CLI | `.devcontainer/devcontainer.json` |
| Entorno Python y dependencias del proyecto | `.devcontainer/preparar.sh` |
| Extensiones oficiales de Python y PR | `.devcontainer/devcontainer.json` |
| Guía y lote abiertos al crear el espacio | `customizations.codespaces.openFiles` |
| Acciones del menú Terminal → Run Task | `.vscode/tasks.json` |
| Inicio del visor en cada arranque | `postStartCommand` y `scripts/codespaces.py` |
| Vista validada al recargar | `scripts/servir.py`; salidas en `build/visor/` |

La vista de trabajo no modifica los archivos exportados de `web/` ni publica Pages. Si los CSV están a medio editar, el entorno sigue abriendo para poder corregirlos y la vista informa el error. El visor se sirve por el puerto 8000, privado por defecto en Codespaces.

## Prueba de aceptación en GitHub

La configuración y sus scripts se verificaron fuera de Codespaces; la creación de una máquina remota real requiere esta comprobación de la cuenta/organización.

- [ ] Abrir un Codespace nuevo desde el navegador con la rama actualizada.
- [ ] Confirmar que termina la preparación automática sin pedir instalaciones al estudiante.
- [ ] Ver la guía de primeras actividades abierta.
- [ ] Ejecutar **Callejero: Validar datos** y **Callejero: Ejecutar pruebas**.
- [ ] Abrir **Ports → 8000 → Open in Browser**, conservando visibilidad privada.
- [ ] En una rama de ensayo, guardar una consulta; recargar y comprobar su aparición.
- [ ] Introducir un error de formato temporal, comprobar que el visor lo explica y corregirlo.
- [ ] Ejecutar **Callejero: Generar entrega** y abrir el informe en el explorador remoto. Descargarlo desde allí si se necesita compartirlo.
- [ ] Hacer commit y push de un cambio de práctica y abrir un PR desde el navegador.
- [ ] Después de incorporar los workflows a main, comprobar en un PR de práctica el comentario con imagen y su actualización ante un error. Ver `VISTAS_PREVIAS.md`.
- [ ] Detener y reabrir el mismo Codespace; comprobar el reinicio del visor y la persistencia de archivos.

Registrar fecha, cuenta de prueba y resultado mediante una referencia apropiada. Si falla la instalación remota, el supervisor revisa el log y la red/políticas de GitHub; no traslada la configuración a la computadora del estudiante.

## Preparación de las actividades

Completá la configuración institucional y regenerá la propuesta antes de la primera sesión. Revisá [Primeras actividades](ACTIVIDADES_INICIALES.md), prepará las referencias publicables y comprobá que los IDs asignados sigan disponibles. Si ya están trabajados, elegí reemplazos de dificultad equivalente y anotá los IDs en la ficha. No asignes automáticamente las primeras cinco filas de un lote.

Antes del primer guardado, prepará una rama de práctica para las fichas; acompañá los primeros commits y envíos hasta presentar Git al estudiante. Reservá acompañamiento para las primeras dos semanas, especialmente los últimos 20 minutos para guardar y subir. Si no podés estar en una actividad nueva, el estudiante puede continuar su ficha o comparar los casos resueltos; la edición y el primer envío esperan al acompañamiento. Registrá los apoyos necesarios en sesiones 5, 10 y 15 y ajustá el ritmo.

La evidencia para clasificar el homenaje puede faltar aunque el nombre esté documentado: se permite `sin_confirmar`. El supervisor conserva las verificaciones espaciales de las 39 calles y las conformidades; el estudiante explica las limitaciones. Programar es opcional. Ver [evaluación con ejemplos observables](EVALUACION_ESTUDIANTE.md).

## Acompañamiento didáctico

Durante la primera hora, abrir la actividad, leer el caso y formular una pregunta en una ficha. La validación se presenta en la sesión 2; registrar una fila y corregir un error se practican después. Introducir rama, commit, push y PR gradualmente, con un primer envío acompañado en sesiones 6–10. No pedir que memorice comandos para instalar paquetes.

Una consulta bien planteada cuenta como evidencia de aprendizaje. Los comentarios del PR deben explicar qué dato o razonamiento falta. Evitar resolver todas las dudas por él o medir progreso solo por el total completado.

Los cambios en `.devcontainer/` y `.vscode/` también requieren revisión del responsable de código, pues definen qué se ejecuta al abrir el entorno. El operador municipal conserva el ensayo de AutoCAD en copia; Codespaces no ejecuta AutoCAD.

Referencias: [configuración de Python en Codespaces](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces), [archivos de bienvenida](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/automatically-opening-files-in-the-codespaces-for-a-repository) y [puertos reenviados](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace).
