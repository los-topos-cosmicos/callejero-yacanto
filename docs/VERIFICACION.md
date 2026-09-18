# Verificación del paquete — 18 de septiembre de 2026

## Resultados comprobados

| Control | Resultado |
|---|---|
| `python scripts/validar.py` | Correcto: 251 calles, 1.102 rótulos, 6 propuestas de conservación, 4 consultas, 241 sin revisar, 0 conformidades |
| `python -m unittest discover -s tests -v` | 18 pruebas correctas: 17 de datos/generación/extracción y 1 de estructura LISP |
| Exportación de un cambio sintético con aprobación exacta | Los 9 rótulos de Av Jose Marrero reciben la misma grafía de prueba; acento intacto en UTF-8 y CP1252 |
| Propuesta sin conformidad / conformidad obsoleta | Excluida del archivo aprobado / validación rechazada |
| Generación del ejemplo | PDF, CSV, GeoJSON, gráfico, LISP, TXT, acta vacía y manifiesto generados desde datos validados |
| Propuesta formal | 5 páginas renderizadas y revisadas visualmente; fuentes incorporadas al PDF |
| Informe de ejemplo | 3 páginas renderizadas y revisadas visualmente |
| GeoJSON | 251 registros; geometrías nulas; no se publican posiciones como verificadas |
| Workflows YAML | Parseados; validación con token de solo lectura; Pages condicionado y manual |
| Script de primer push | Sintaxis Bash comprobada; no ejecutado contra GitHub |
| JavaScript del visor | Sintaxis comprobada con Node; datos y DOM revisados en el código |

## Límites de la verificación

No se ejecutó el AutoLISP dentro de AutoCAD, no se reextrajo el DWG real ni se certificaron los handles contra él. El extractor se probó con un DXF sintético que incluye texto con formato.

La prueba automatizada de navegador no pudo ejecutarse: faltaba el ejecutable y su descarga no estuvo disponible. Revisar búsqueda, filtro y visualización local al abrir el visor; no se declara una prueba visual de navegador superada.

No se subió el repositorio, no se crearon issues remotas y no se activaron reglas ni GitHub Pages. Los workflows requieren su primera ejecución en GitHub para confirmar el entorno remoto y las políticas de la organización.

Estos resultados describen esta versión del paquete. Regenerar y repetir los controles después de modificar datos, conformidades o herramientas.
