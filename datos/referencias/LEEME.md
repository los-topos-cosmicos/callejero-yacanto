# Referencias externas para contrastar el inventario

Las instantáneas son **referencias de atributos**, separadas de `datos/crudo/`. No reemplazan los datos recibidos, no certifican la localidad del DWG y no convierten geometrías externas en posiciones del plano. Los códigos nacionales nunca sustituyen los IDs de tres cifras del proyecto.

- `georef_villa_yacanto.json`: respuesta completa de Georef para la localidad censal `14007360`, departamento `14007`, Córdoba. 272 registros; incluye vías sin nombre.
- `indec2022_villa_yacanto.json`: respuesta de atributos del Marco Geoestadístico Nacional 2022, publicada en el portal de INDEC. 296 tramos y 60 combinaciones distintas de nombre/tipo. Los tramos repetidos no son nombres nuevos. Se excluyeron geometrías mediante `propertyName`; los nulos de este archivo no son los del inventario del proyecto.
- `fuentes.json`: URL, fecha, alcance y huellas de las instantáneas; también identifica documentos municipales y pistas bibliográficas pendientes de cotejo.

**Cita:** Instituto Nacional de Estadística y Censos (2022). Marco Geoestadístico Nacional. https://portalgeoestadistico.indec.gob.ar/ . Para Georef: Servicio de Normalización de Direcciones y Unidades Territoriales de Argentina, consulta 2026-10-24. La licencia MIT del código no se extiende a las fuentes externas. Consultar sus condiciones de uso; no se atribuye una licencia nueva ni se publica cartografía parcelaria.

[Metadatos de la capa 2022](https://portalgeoestadistico.indec.gob.ar/geoportal/documents/metadato_vias_de_circulacion.pdf). [Ayuda del nomenclador](https://viascirculacion.indec.gob.ar/?contenido=ayuda): los nombres de búsqueda no conservan tildes ni caracteres especiales. Por eso una coincidencia normalizada es solamente un candidato. La ausencia en estas fuentes no demuestra que la vía no exista.

## Reproducir la consulta y el contraste

Las URLs exactas están en `fuentes.json`. Descargar a una carpeta nueva, verificar total y localidad y comparar las huellas antes de actualizar una instantánea. Nunca reemplazar silenciosamente un archivo de referencia.

Ejecutar `python scripts/auditar_referencias.py`. Produce `build/cruce_referencias.csv`, conserva registros sin coincidencia y muestra códigos distintos si un nombre tiene varios candidatos. No hace búsquedas aproximadas, no expande iniciales y no modifica los lotes. CI ejecuta el contraste y guarda la salida en el artefacto de revisión. El manifiesto de entrega incluye las huellas de estas referencias.

## Jerarquía de evidencia

1. Documento municipal descargado y cotejado: identifica el texto publicado y su alcance. Una referencia a una calle dentro de otro trámite no es necesariamente una ordenanza de denominación.
2. Referencia nacional: permite contrastar nombre y tipo, con límites de fecha, cobertura y normalización. La identidad física con el registro del DWG requiere verificación aparte.
3. Criterio ortográfico: justifica una propuesta tipográfica, sin atribuir un homenaje.
4. Índice/transcripción de terceros: sirve para localizar un documento. Si no se obtuvo el original, se mantiene como pista y no como denominación certificada.

Se localizaron las ordenanzas 804–813/2018 y 920–921/2020 en índices públicos. El anexo A del nomenclador 920/2020 y los planos de denominaciones no se pudieron cotejar: el servidor provincial devolvió 403. Deben pedirse al referente por número y fecha, con sus modificaciones. No se infiere vigencia ni inexistencia de reformas a partir de una búsqueda sin resultados.
