# Revisión del lote 03 · 021–040

Consulta: 2026-10-24. Revisión de los registros recibidos; no es una conformidad municipal ni una certificación de identidad espacial.

Resultado: **5 propuestas, 15 consultas, 0 cambios de escritura** (0 rótulos potenciales de simulación). Se preservan todos los IDs y nombres crudos.

Fuentes reproducibles: [registro y límites](../../datos/referencias/LEEME.md), [URLs y huellas](../../datos/referencias/fuentes.json). INDEC y Georef son referencias nacionales; sus nombres normalizados no prueban el referente ni la correspondencia con los handles del DWG. Las pistas de ordenanzas no cotejadas se usan únicamente para pedir los originales.

Los nombres parecidos y traducciones permanecen separados. Una propuesta de conservación no afirma haber encontrado una ordenanza. Cuando el tipo no tiene respaldo suficiente se conserva la pregunta; no se rellena calle por defecto.

| ID / recibido | Resultado | Motivo o pregunta para revisión |
|---|---|---|
| 021 · Av. Los Sauces | En consulta | El inventario dice Av. Los Sauces y la referencia nacional LOS SAUCES figura como CALLE (1400736001245). ¿Son la misma vía y cuál es su tipo vigente? No eliminar Av. ni unirlas automáticamente. |
| 022 · Av. Virgen | En consulta | ¿Av. Virgen es una denominación completa o un rótulo abreviado? Confirmar documento y trazado; no fusionar con IDs 015, 023 o 062. |
| 023 · Av. Virgen de la Merced | Av. Virgen de la Merced | ¿Qué documento confirma Av. Virgen de la Merced y su relación con Av. Virgen (022) o de la Merced (062)? No fusionar registros por compartir palabras. Conservación sin renombre. |
| 024 · Avenida Ascasubi | Avenida Ascasubi | El prefijo indica avenida. ¿Ascasubi refiere a una persona, una localidad u otra denominación? No añadir nombre de pila; pedir entrada exacta del nomenclador y plano. Conservación sin renombre. |
| 025 · Avenida Yacanto | En consulta | El índice de la ordenanza 804/2018 menciona Av. Yacanto. ¿El original y su plano F350 identifican la misma vía del ID 025? Cotejar también el Anexo A de 920/2020 antes de proponer un renombre. |
| 026 · Balnearia | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Balnearia y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 027 · Bartolome Mitre | En consulta | Candidato ortográfico: Bartolomé Mitre. ¿Qué documento municipal confirma esa grafía y el tipo de vía? No se adopta el nombre de una persona como prueba de la denominación. |
| 028 · Belgrano | Belgrano | No expandir Belgrano ni fusionar con Manuel Belgrano (154): son registros separados hasta contrastar el trazado. Cotejo espacial municipal pendiente. |
| 029 · Bell Ville | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Bell Ville y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 030 · Bella Vista | Bella Vista | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |
| 031 · Benjamin Franklin | En consulta | Candidato ortográfico: Benjamín Franklin. ¿La denominación municipal usa esa forma u otra? Confirmar tipo de vía; no traducir nombres propios por intuición. |
| 032 · Bosque Alto | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Bosque Alto y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 033 · Brasil | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Brasil y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 034 · Buchardo | Buchardo | Conservar Buchardo: la referencia nacional distingue BUCHARDO (calle 1400736000065) de AV BOUCHARD (1400736000035). No sustituir un apellido ni fusionar vías por parecido. Cotejo espacial municipal pendiente. |
| 035 · Buenos Aires | En consulta | El índice de la ordenanza 921/2020 menciona Buenos Aires en La Huertilla. ¿El original y sus manzanas corresponden al ID 035? Pedir plano; no adoptar la coincidencia textual como identidad espacial. |
| 036 · C. Velez | En consulta | ¿Qué significa C. en C. Velez y cuál es el tipo de vía? La referencia nacional incluye JUAN CARLOS VELEZ (1400736001225), pero no justifica expandir esta inicial ni unir con 118. |
| 037 · Calchaqui | En consulta | Candidato ortográfico: Calchaquí. ¿Qué grafía y tipo fija el documento municipal? No atribuir automáticamente un homenaje a una región o pueblo. |
| 038 · Capilla del Monte | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Capilla del Monte y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 039 · Carcaraña | En consulta | ¿El documento municipal confirma Carcaraña o una variante como Carcarañá? La semejanza con un topónimo no basta para cambiar la grafía ni determinar el tipo de vía. |
| 040 · Carlos Arcusin | En consulta | ¿Qué documento municipal confirma el nombre completo, grafía y tipo de vía de Carlos Arcusin? No agregar tildes a un apellido sin comprobar su escritura. |

## Cierre de esta revisión

Las preguntas anteriores se entregan agrupadas al referente. Solicitar la entrada y plano del nomenclador (Anexo A de 920/2020 y sus modificaciones), el tipo de vía y, cuando corresponda, el texto de la ordenanza de denominación. No se enviaron mensajes a terceros.

Al obtener un documento, registrar su referencia publicable y revisar la relación entre vía y registro; cambiar una consulta a propuesta no genera conformidad. El supervisor registra por separado cualquier decisión municipal sobre el texto exacto.

Comprobación: `python scripts/validar.py`; `python scripts/auditar_referencias.py`; generación de entrega en carpeta nueva. Las consultas no entran al archivo de cambios aprobados.
