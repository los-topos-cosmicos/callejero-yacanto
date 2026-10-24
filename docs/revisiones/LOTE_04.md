# Revisión del lote 04 · 041–060

Consulta: 2026-10-24. Revisión de los registros recibidos; no es una conformidad municipal ni una certificación de identidad espacial.

Resultado: **3 propuestas, 17 consultas, 1 cambios de escritura** (14 rótulos potenciales de simulación). Se preservan todos los IDs y nombres crudos.

Fuentes reproducibles: [registro y límites](../../datos/referencias/LEEME.md), [URLs y huellas](../../datos/referencias/fuentes.json). INDEC y Georef son referencias nacionales; sus nombres normalizados no prueban el referente ni la correspondencia con los handles del DWG. Las pistas de ordenanzas no cotejadas se usan únicamente para pedir los originales.

Los nombres parecidos y traducciones permanecen separados. Una propuesta de conservación no afirma haber encontrado una ordenanza. Cuando el tipo no tiene respaldo suficiente se conserva la pregunta; no se rellena calle por defecto.

| ID / recibido | Resultado | Motivo o pregunta para revisión |
|---|---|---|
| 041 · Carlos Ballestrini | En consulta | ¿El apellido oficial es Ballestrini, Balestrini u otra variante? Pedir documento de denominación y tipo de vía; no sustituir consonantes por usos de cartografía o anuncios. |
| 042 · Carmen Marcos Gigena | En consulta | La referencia nacional usa CJAL CARMEN GIGENA (1400736001180), mientras el registro dice Carmen Marcos Gigena. ¿Es la misma vía? Confirmar nombre completo y trazado antes de eliminar Marcos o agregar Concejal. |
| 043 · Carquejilla | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Carquejilla y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 044 · Catania | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Catania y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 045 · Cementerio | En consulta | ¿Cementerio es una calle con nombre propio, un acceso o un rótulo de equipamiento? La ordenanza 1099/2025 ubica el cementerio en Los Cedros; no demuestra que este ID sea una vía denominada Cementerio. |
| 046 · Charcal | En consulta | ¿Charcal y Charcas (047) son vías distintas o variantes de extracción? La referencia nacional contiene CHARCAS; cotejar handles y plano antes de corregir o fusionar. |
| 047 · Charcas | Charcas | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |
| 048 · Che Guevara | En consulta | ¿Qué documento confirma Che Guevara como denominación y tipo de vía? No reemplazar el apodo por un nombre civil sin respaldo municipal. |
| 049 · Chilecito | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Chilecito y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 050 · Colombia | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Colombia y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |
| 051 · Colonias Unidas | En consulta | ¿Colonias Unidas es la denominación completa? Confirmar tipo y referente documental; no asociar por defecto con una localidad u organización homónima. |
| 052 · Concejal Alfredo Busto | En consulta | ¿El documento dice Concejal Alfredo Busto o existe otra grafía del apellido? Confirmar denominación y tipo; no corregir a Bustos sin evidencia. |
| 053 · Concejal Palacios | En consulta | ¿Qué documento confirma Concejal Palacios y su tipo de vía? No añadir un nombre de pila ni inferir una identidad de registros institucionales actuales. |
| 054 · Concejal Peñaloza | En consulta | La referencia nacional registra ALFREDO PENALOZA (1400736000020). ¿Corresponde a Concejal Peñaloza del ID 054? No añadir Alfredo ni sustituir el título sin cotejo municipal y espacial. |
| 055 · Cordoba | Córdoba | Propuesta ortográfica limitada: Cordoba → Córdoba. No se desarrolla identidad ni se certifica el referente. |
| 056 · Corrientes | Corrientes | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |
| 057 · Cosquin | En consulta | Candidato ortográfico: Cosquín. ¿Qué documento confirma grafía y tipo de vía? La escritura de una localidad homónima no acredita la intención municipal. |
| 058 · Cr. San Agustin | En consulta | ¿Qué significa Cr. en Cr. San Agustin? Confirmar texto completo y tipo de vía; no expandir a Coronel, Contador u otro título. Revisar la posible tilde de Agustín con la fuente. |
| 059 · Cristiane Quirino | En consulta | ¿Qué documento confirma la grafía Cristiane Quirino y el tipo de vía? No traducir ni modificar un nombre posiblemente extranjero sin respaldo de denominación. |
| 060 · Cruz del Eje | En consulta | ¿Qué entrada del nomenclador y plano municipal confirma la grafía Cruz del Eje y su tipo de vía? No hay coincidencia textual en las dos instantáneas nacionales; esa ausencia no demuestra inexistencia ni autoriza a cambiar el nombre. |

## Cierre de esta revisión

Las preguntas anteriores se entregan agrupadas al referente. Solicitar la entrada y plano del nomenclador (Anexo A de 920/2020 y sus modificaciones), el tipo de vía y, cuando corresponda, el texto de la ordenanza de denominación. No se enviaron mensajes a terceros.

Al obtener un documento, registrar su referencia publicable y revisar la relación entre vía y registro; cambiar una consulta a propuesta no genera conformidad. El supervisor registra por separado cualquier decisión municipal sobre el texto exacto.

Comprobación: `python scripts/validar.py`; `python scripts/auditar_referencias.py`; generación de entrega en carpeta nueva. Las consultas no entran al archivo de cambios aprobados.
