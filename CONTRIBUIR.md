# Cómo trabajar en un lote

El estudiante edita `datos/lotes/lote-NN.csv`. No modifica `datos/crudo/`, `datos/conformidad.csv` ni las herramientas sin una tarea revisada por el supervisor.

## Formato

Guardar como CSV UTF-8, separado por comas, con la cabecera exacta. Usar comillas CSV si una nota contiene comas. No dejar que una planilla elimine ceros de los IDs: `008` es distinto de `8`.

| Columna | Contenido |
|---|---|
| `id`, `nombre_crudo` | No cambiar; identifican el registro recibido |
| `nombre` | Grafía propuesta; vacío si se consulta |
| `tipo` | calle, avenida, pasaje, camino, ruta, bulevar o diagonal |
| `homenaje` | persona, lugar, fecha u otro; clasificación provisional, no prueba de identidad |
| `estado` | vacío, propuesta o en_consulta |
| `nota` | Motivo del cambio o pregunta concreta, hasta 500 caracteres |
| `fuente` | Ordenanza, referencia documental, URL o criterio verificable; hasta 500 caracteres |

**`propuesta`** requiere nombre, tipo, homenaje y fuente/criterio. Si cambia el nombre, requiere nota. Conservar la grafía también puede ser una propuesta, indicando que el referente histórico sigue por confirmar.

**`en_consulta`** requiere una pregunta y deja nombre vacío. No inventar a qué Alsina se refiere una calle ni convertir coincidencias históricas en una fuente municipal.

**`aprobada`** no se escribe en el lote. El supervisor registra en `datos/conformidad.csv` el ID, el nombre original, el nombre exacto aprobado, la fecha y una referencia de decisión. Si el nombre cambia después, la validación falla hasta volver a revisar la conformidad.

La rutina CAD solo admite texto plano. Por eso se rechazan `|`, barra invertida, llaves, `%`, caracteres invisibles y nombres que no se pueden representar en el auxiliar Windows-1252. Esto es una restricción del procedimiento de entrega elegido; no significa que todos los DWG sean incapaces de contener Unicode. Un caso válido que no entra en ese contrato se eleva a revisión manual.

## Una contribución, toda en el navegador

1. Abrir el Codespace y crear una rama con el nombre de la tarea.
2. Editar pocas filas y guardar.
3. Usar **Terminal → Run Task → Callejero: Validar datos**.
4. Revisar el diff en **Source Control**, seleccionar los archivos, escribir el mensaje y hacer **Commit**.
5. Usar **Publish Branch / Push** y abrir un PR en GitHub.

La [guía de Codespaces](docs/CODESPACES_ESTUDIANTE.md) detalla cada clic. No hay instalaciones ni claves que configurar en la computadora del estudiante.

En el PR, explicar las fuentes y enlazar la issue. Usar `Closes #N` solo si se completa toda la tarea. En Actions → ejecución → Artifacts se descarga la validación y la entrega generada. Si la validación falla, el artefacto conserva sus mensajes y no se exportan datos inválidos.

El comentario de vista previa muestra las filas modificadas con un círculo naranja. Si falla un control, indica cómo revisar el error. Ver [cómo leer la devolución](docs/VISTAS_PREVIAS.md).

El supervisor revisa contenido, no solo el check verde. Una fuente escrita puede ser débil: la validación comprueba estructura y coherencia, no verdad histórica ni competencia legal de quien decide.
