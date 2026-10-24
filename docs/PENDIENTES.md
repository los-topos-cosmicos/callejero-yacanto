# Ver qué falta después de incorporar un PR

Un PR incorporado significa que una revisión quedó guardada. **Una fila en consulta sigue pendiente y una propuesta todavía necesita decisión municipal.** El informe se calcula desde los CSV y las conformidades actuales, sin usar el número de PRs como medida de resolución.

## En Codespaces

1. Con ayuda al principio, volvé a `main` y traé los cambios incorporados mediante **Source Control → … → Pull**. No descartes trabajo sin subir; pedí ayuda si hay cambios pendientes.
2. Ejecutá **Terminal → Run Task → Callejero: Ver pendientes**.
3. Abrí la ruta a `PENDIENTES.md` que imprime la tarea. Cada ejecución crea una carpeta nueva en `build/pendientes-…/`, con fecha UTC y huellas de los datos.
4. Abrí `pendientes_de_revision.csv` y buscá el lote o ID que querés continuar. Contiene la pregunta o motivo, fuente, responsable por rol y siguiente paso.

También se puede ejecutar `python scripts/pendientes.py`. **Callejero: Generar entrega** incluye el mismo informe y sus CSV dentro del paquete; el manifiesto conserva las huellas de esos archivos.

## Qué significa cada lista

| Archivo | Qué responde |
|---|---|
| `PENDIENTES.md` | Cuántos registros quedan en cada estado y cómo continuar |
| `resumen_por_lote.csv` | Qué lotes tienen filas sin revisar, consultas o propuestas sin conformidad |
| `pendientes_de_revision.csv` | Qué falta en cada ID: revisar, obtener evidencia o decidir sobre la propuesta |
| `verificacion_espacial.csv` | Qué registros están fuera del recorte heredado y necesitan cotejo espacial |
| `metadatos_por_confirmar.csv` | Qué filas revisadas conservan tipo u homenaje sin confirmar |
| `verificaciones_proyecto.csv` | Qué se declara o sigue pendiente respecto de localidad, CRS, DWG y CAD |
| `pendientes.json` | Los mismos datos, fecha y huellas, para comprobación automática |

Cada nombre sin conformidad aparece una vez en la lista principal. Las listas espacial y de metadatos pueden contener el mismo ID: son dimensiones distintas, no calles adicionales. Una conformidad sobre el texto no certifica el referente histórico ni la georreferenciación.

## Cómo se cierra un caso

- **Sin revisar → consulta:** se identificó una pregunta; falta resolverla.
- **Consulta → propuesta:** llegó evidencia y se documentó un texto; falta revisión y decisión municipal.
- **Propuesta → conformidad registrada:** el supervisor registró una decisión real sobre el texto exacto en `datos/conformidad.csv`. El ID sale de la lista de nombres pendientes al regenerar.
- Si cambia el nombre después de una conformidad, la validación falla hasta revisar esa decisión. El informe no oculta el problema ni genera una lista nueva sobre datos inválidos.

El estudiante puede completar su aprendizaje con consultas abiertas. Resolverlas y gestionar decisiones institucionales no es una cuota individual del estudiante.

## Desde GitHub, sin abrir Codespaces

Tras cada incorporación a `main`, **Actions → Validar callejero → ejecución de esa versión → Artifacts → revision-…** contiene `build/pendientes/PENDIENTES.md` y los CSV. En un PR, el informe corresponde a los datos que validó esa ejecución, no a una aprobación futura. Comprobar la versión y la fecha del informe; los artefactos tienen retención limitada y conviene descargar los que se necesiten conservar.

No hay que esperar a incorporar todos los PRs: el informe funciona durante la revisión y después. Cero filas sin revisar no significa cero consultas, cero decisiones pendientes ni prueba CAD realizada.
