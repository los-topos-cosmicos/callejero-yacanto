# Datos y estados

`crudo/calles_crudo.csv` y `crudo/etiquetas.csv` se conservaron sin modificar desde el último ZIP recibido. `crudo/manifest.json` registra sus huellas. No regenerar IDs ni reemplazar la base en mitad del trabajo.

- 251 registros de calle, no necesariamente 251 vías oficialmente distintas.
- 1.102 rótulos asociados mediante handles únicos en estos CSV.
- 39 registros con `en_mapa=no`: fuera del recorte heredado. La causa no está verificada.
- `x_gk`, `y_gk`, `lat`, `lon` conservan los nombres de columna recibidos. Ni esas etiquetas ni sus valores demuestran un CRS correcto. Los valores geográficos no se usan para geometrías publicadas.

Estados del trabajo: vacío (sin revisar), `propuesta`, `en_consulta`. El estado derivado `aprobada` exige una fila válida en `conformidad.csv`; no certifica coordenadas ni contenido biográfico.

Conformidad: `id,nombre_crudo,nombre_aprobado,fecha,referencia`. La fecha es AAAA-MM-DD. La referencia puede ser un número interno de acta/expediente; no subir firmas, datos personales ni documentos de circulación restringida. El CSV no autentica a una autoridad: la evidencia se custodia fuera del repositorio y el acceso se protege con reglas y revisión.

Una nueva extracción se audita con `scripts/extraer.py` en una carpeta separada. Si se acepta una nueva base, el supervisor prepara una migración explícita de IDs, lotes y conformidades. El extractor no hace esa migración automáticamente.
