# Verificación del paquete — 18 de septiembre de 2026

## Resultados comprobados

| Control | Resultado |
|---|---|
| `python scripts/validar.py` | Correcto: 251 calles, 1.102 rótulos, 6 propuestas de conservación, 4 consultas, 241 sin revisar, 0 conformidades |
| `python -m unittest discover -s tests -v` | 36 pruebas correctas: 17 de datos/generación/extracción, 1 de estructura LISP, 5 de Codespaces/servidor, 7 de selección visual y 6 de publicación con API simulada |
| Exportación de un cambio sintético con aprobación exacta | Los 9 rótulos de Av Jose Marrero reciben la misma grafía de prueba; acento intacto en UTF-8 y CP1252 |
| Propuesta sin conformidad / conformidad obsoleta | Excluida del archivo aprobado / validación rechazada |
| Generación del ejemplo | PDF, CSV, GeoJSON, gráfico, LISP, TXT, acta vacía y manifiesto generados desde datos validados |
| Propuesta formal | 5 páginas renderizadas y revisadas visualmente; fuentes incorporadas al PDF |
| Informe de ejemplo | 3 páginas renderizadas y revisadas visualmente |
| GeoJSON | 251 registros; geometrías nulas; no se publican posiciones como verificadas |
| Workflows YAML | Parseados; validación de solo lectura; publicador separado mediante workflow_run; Pages condicionado y manual |
| Preparación de Codespaces | JSON y Bash comprobados; tareas apuntan a comandos existentes |
| Servidor de vista | Arranque y reejecución idempotente comprobados; un CSV inválido devuelve 503 y se recupera al corregirlo |
| Menú de tareas | Acciones de validación, vista y entrega ejecutadas; genera una carpeta nueva por entrega |
| JavaScript del visor | Sintaxis comprobada con Node; datos y DOM revisados en el código |
| Resaltado del PR | Una modificación de nota resalta solo su ID; reordenar filas no suma avance; conformidades incluidas en la comparación |
| Publicador de imágenes | API simulada: casos correctos, errores, forks, versiones obsoletas y artefactos inesperados; sin escrituras reales |
| Ubicación compartida | Redirección de Maps comprobada: Villa Yacanto, Córdoba, Argentina; referencia separada de la georreferenciación |

## Límites de la verificación

No se ejecutó el AutoLISP dentro de AutoCAD, no se reextrajo el DWG real ni se certificaron los handles contra él. El extractor se probó con un DXF sintético que incluye texto con formato.

La prueba automatizada de navegador no pudo ejecutarse: faltaba el ejecutable y su descarga no estuvo disponible. Revisar búsqueda, filtro y visualización local al abrir el visor; no se declara una prueba visual de navegador superada.

El usuario ya subió el repositorio base. Esta actualización se preparó sobre main, commit 1d220779aa62fdaf761af2004a965a2629073332, que coincide con el ZIP adjunto. No se pudo subir la actualización desde este entorno por falta de credenciales de escritura. No se crearon issues ni se modificaron ajustes remotos de Codespaces, facturación, permisos o Pages.

Estos resultados describen esta versión del paquete. Regenerar y repetir los controles después de modificar datos, conformidades o herramientas.

## Alcance de la prueba de Codespaces

Se probaron en este entorno los scripts que se ejecutarán en Codespaces y las respuestas HTTP de su visor. Se comprobó que la vista usa los datos recién guardados, bloquea una exportación inválida y no sirve los archivos de configuración ni los CSV crudos. No se modificó ningún CSV del estudiante.

No se creó una máquina de GitHub Codespaces ni se construyó la imagen Docker aquí. Quedan para el supervisor la primera apertura real, la instalación remota desde los registros de imágenes/paquetes, la disponibilidad según cuenta y plan y la comprobación de botones en el editor web. Ver la prueba de aceptación de `CODESPACES_SUPERVISOR.md`.

El PDF actualizado conserva cinco páginas y fue renderizado y revisado visualmente. El README contiene la imagen de bienvenida y un diagrama Mermaid; su sintaxis está escrita para GitHub, sin afirmar que se haya renderizado en el repositorio remoto antes de aplicar la actualización.

## Integración del ZIP recibido

El complemento `vista-previa-pr.zip` requería primero la actualización de Codespaces y traía un workflow distinto del archivo suelto. Este paquete combina ambas funciones sobre la misma base del repositorio; se aplica una única actualización.

Se revisaron visualmente los gráficos con una fila y con muchas filas destacadas. La leyenda se colocó fuera del dibujo para no tapar puntos; el contorno naranja conserva el color de estado. El PDF incorpora Villa Yacanto y el enlace compartido, manteniendo cinco páginas.

Las 6 pruebas del publicador usan respuestas simuladas, no la API autenticada. No se publicó ninguna imagen ni comentario desde este entorno. La comprobación real se hace después de incorporar los workflows a main; ver `VISTAS_PREVIAS.md`.
