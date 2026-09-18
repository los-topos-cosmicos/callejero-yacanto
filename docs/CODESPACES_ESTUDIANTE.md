# Tu escritorio de trabajo está en el navegador

Vas a usar **GitHub Codespaces** durante toda la pasantía. Tu computadora solo abre el navegador: Python, Git, las dependencias y el visor se preparan automáticamente en GitHub. No instales programas ni generes claves para este proyecto.

## 1. Entrar por primera vez

1. Iniciá sesión con tu propia cuenta GitHub y aceptá la invitación al repositorio si la recibiste.
2. Abrí [crear el Codespace del callejero](https://codespaces.new/los-topos-cosmicos/callejero-yacanto?quickstart=1). También llegás desde el repositorio con **Code → Codespaces → Create codespace on main**.
3. Si aparece la elección de máquina, usá **2 cores**. Si pide facturación, pago o permisos que no tenés, avisá al supervisor: él prepara ese acceso antes de tu primera sesión.
4. Esperá la preparación automática. La primera apertura puede tardar varios minutos. Elegí **Open in Browser** si GitHub ofrece varios editores.
5. Vas a ver esta guía y `datos/lotes/lote-02.csv`. El lote 01 se abre desde la columna izquierda para estudiar los ejemplos.

Los próximos días, abrí **el mismo Codespace** desde https://github.com/codespaces. Tus archivos guardados permanecen en ese espacio mientras exista; el commit y el push son los que conservan el trabajo en el repositorio.

## 2. Reconocer las cuatro zonas

| Zona | Para qué sirve | Qué mirar |
|---|---|---|
| Explorer / Explorador, a la izquierda | Abrir archivos | `datos/lotes/` y `docs/` |
| Editor, en el centro | Cambiar el CSV o leer la guía | La cabecera y la fila asignada |
| Terminal y tareas, abajo | Ver la validación | Mensaje y fila del error |
| Source Control / Control de código fuente | Comparar, guardar y subir cambios | Solo los archivos de tu tarea |

Una **rama** es una línea de trabajo separada de `main`. Un **commit** guarda una versión con un mensaje. Un **push** la sube al repositorio. Un **PR** es una solicitud de revisión; el supervisor lo revisa antes de incorporar el trabajo.

## 3. Crear la rama de tu tarea

1. Hacé clic en el nombre de la rama abajo a la izquierda (`main` la primera vez).
2. Elegí **Create new branch / Crear nueva rama**.
3. Escribí, por ejemplo, `lote-02-primer-grupo`.
4. Confirmá que ese nombre aparece abajo antes de editar.

Al empezar una nueva tarea, el supervisor te ayuda a volver a `main` y traer la versión actual desde **Source Control → … → Pull**. Si quedan cambios sin subir, no los descartes: terminá o pedí revisión primero.

## 4. Revisar pocas calles y guardar

Abrí el lote indicado. Trabajá en 5–10 filas como máximo por grupo; no es una cuota diaria. Conservá `id` y `nombre_crudo`. Para cada caso:

- Si tenés un criterio verificable, completá nombre, tipo, homenaje, `propuesta`, nota y fuente.
- Si falta información, dejá `nombre` vacío, escribí `en_consulta` y una pregunta concreta en nota.
- Si aún no lo trabajaste, dejá vacíos los campos de revisión.

El editor guarda automáticamente después de un segundo. Antes de validar podés usar **File → Save / Archivo → Guardar**. No uses una planilla local: así evitás perder los ceros iniciales de los IDs.

## 5. Validar y entender el resultado

1. Abrí **Terminal → Run Task / Ejecutar tarea**. Si el menú está contraído, abrí el menú principal de la esquina superior izquierda.
2. Elegí **Callejero: Validar datos**.
3. Leé la terminal que aparece abajo.

También sirve abrir la paleta con **Ctrl+Shift+P** (Windows/Linux) o **Cmd+Shift+P** (Mac), buscar **Tasks: Run Task** y elegir la tarea. Esto ocurre dentro del navegador.

- `"valido": true`: las reglas de formato y coherencia pasan. Todavía hace falta revisión humana de las fuentes.
- `"valido": false`: leé la fila indicada, corregí y repetí. Un error es una indicación de qué revisar, no una calificación.

Ejemplo: si el mensaje dice que falta la fuente, explicá de dónde sale tu propuesta. No inventes una referencia para obtener un check verde; si no hay evidencia suficiente, cambiá el caso a consulta.

## 6. Abrir el visor

1. Buscá **Ports / Puertos** en el panel inferior.
2. En el puerto **8000**, hacé clic en **Open in Browser / Abrir en navegador**.
3. Guardá tus cambios y recargá esa pestaña para verlos.

No escribas `localhost:8000` en el navegador de tu computadora: usá el enlace que te da Codespaces. El puerto se mantiene **Private / Privado**. Si no aparece, ejecutá la tarea **Callejero: Iniciar visor**.

Para crear la imagen de avance, ejecutá **Callejero: Actualizar vista y gráfico** y abrí `build/avance.png`. Si los datos no validan, el visor muestra los errores; no oculta el problema con una versión vieja.

## 7. Pedir revisión: commit, push y PR

1. Abrí **Source Control / Control de código fuente** en la barra izquierda.
2. Hacé clic en cada archivo cambiado y leé la comparación: rojo es lo que sale y verde lo que entra.
3. Pulsá **+** junto a los archivos que pertenecen a tu tarea. No agregues archivos ajenos ni conformidades.
4. Escribí un mensaje claro, por ejemplo: `Revisar lote 02 y registrar preguntas sobre dos nombres`.
5. Pulsá **Commit**. Luego **Publish Branch** la primera vez o **Sync Changes / Push** las siguientes.
6. Abrí el repositorio en otra pestaña del navegador. Elegí **Compare & pull request** para esa rama. Si no aparece: **Pull requests → New pull request**, base `main`, compare tu rama.
7. Completá la plantilla: qué revisaste, con qué fuentes y qué dudas quedan. Creá el PR y pedí revisión al supervisor.

GitHub autentica el acceso desde tu Codespace; no hace falta configurar claves SSH ni un token manual. Si aparece una solicitud para crear un fork o un error de permisos, avisá al supervisor para comprobar tu acceso al repositorio.

Al terminar los controles, buscá el comentario **Vista de la revisión**: el círculo naranja marca tus filas modificadas y el color interior conserva su estado. Si hay un error, el comentario te lleva a los controles. [Cómo leer la imagen](VISTAS_PREVIAS.md).

## 8. Incorporar comentarios y terminar el día

Los comentarios del supervisor son parte del trabajo. Corregí los mismos archivos en la misma rama, validá y hacé otro commit y push: el PR se actualiza.

Antes de cerrar la hora:

- Guardá, hacé commit y push del avance, aunque quede un PR en borrador.
- Escribí qué hiciste, qué dudás y cuál es el siguiente paso en la bitácora.
- Abrí https://github.com/codespaces y elegí **… → Stop codespace / Detener** en tu espacio. Cerrar la pestaña no lo detiene inmediatamente.

No borres el Codespace como forma de cerrar una sesión. Si tenés que borrarlo al terminar la pasantía, comprobá primero con el supervisor que todo el trabajo esté subido.

## Cuando algo no funciona

| Lo que ves | Qué hacer |
|---|---|
| Sigue preparando el entorno | Esperar la primera instalación; si falla, compartir el mensaje con el supervisor |
| Mensaje de cupo, facturación o acceso | Avisar al supervisor; no instalar herramientas como alternativa |
| La validación marca un error | Leer la fila, corregir o consultar; repetir la tarea |
| El visor no abre | Ejecutar Iniciar visor y usar Ports → 8000 |
| El PR pide cambios | Continuar en la misma rama y subir otro commit |
| No entendés el homenaje de una calle | Escribir una pregunta en `en_consulta` |

Fuente sobre ramas, commits y PR dentro del navegador: [GitHub Codespaces: control de versiones](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace).
