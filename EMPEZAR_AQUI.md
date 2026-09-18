# Todo el trabajo del estudiante se hace en GitHub Codespaces

**Estudiante:** abrí [tu entorno en el navegador](https://codespaces.new/los-topos-cosmicos/callejero-yacanto?quickstart=1) y seguí [la guía paso a paso](docs/CODESPACES_ESTUDIANTE.md). No necesitás instalar Python, Git, VS Code, Docker ni AutoCAD en tu computadora.

**Supervisor:** el repositorio ya está subido. Antes de la primera sesión, revisá acceso y disponibilidad de Codespaces y probá el entorno una vez según [CODESPACES_SUPERVISOR.md](docs/CODESPACES_SUPERVISOR.md).

En Codespaces quedan preparados Python 3.12, las dependencias, las tareas de validación y entrega, el visor y el control de versiones. La guía y el lote de trabajo se abren al crear el espacio. La configuración pertenece al repositorio y se aplica en GitHub.

## Orden para empezar

1. Leer `propuesta/propuesta_pasantia.pdf`: dos meses calendario, una hora por día hábil y 40 sesiones base ajustables al calendario real.
2. Completar lo conocido en `config/proyecto.json` con el supervisor. Regenerar mediante **Terminal → Run Task → Callejero: Regenerar propuesta PDF**.
3. Estudiar el lote 01 y [el caso explicado](docs/APRENDER_CON_UN_CASO.md). No contarlos como producción del estudiante.
4. Asignar la primera tarea de `ISSUES.md`, crear una rama y trabajar en un grupo pequeño del lote 02.
5. Validar, hacer commit y push, y abrir un PR desde el navegador.
6. Al terminar la hora, dejar una bitácora y detener el Codespace desde https://github.com/codespaces.

Los originales, firmas y documentación interna quedan fuera del repositorio público. La prueba en AutoCAD corresponde al operador municipal y se hace sobre una copia: no exige que el estudiante instale nada ni impide iniciar su aprendizaje.

Si querés publicar el visor en Pages, configurá **Settings → Pages → Source: GitHub Actions** y seguí `docs/SUBIR_A_GITHUB.md`. La carpeta `/docs` contiene guías; el workflow publica `web/`.
