# Revisión del lote 01 · 001–010

Consulta: 2026-10-24. Revisión de los registros recibidos; no es una conformidad municipal ni una certificación de identidad espacial.

Resultado: **5 propuestas, 5 consultas, 1 cambios de escritura** (4 rótulos potenciales de simulación). Se preservan todos los IDs y nombres crudos.

Fuentes reproducibles: [registro y límites](../../datos/referencias/LEEME.md), [URLs y huellas](../../datos/referencias/fuentes.json). INDEC y Georef son referencias nacionales; sus nombres normalizados no prueban el referente ni la correspondencia con los handles del DWG. Las pistas de ordenanzas no cotejadas se usan únicamente para pedir los originales.

Los nombres parecidos y traducciones permanecen separados. Una propuesta de conservación no afirma haber encontrado una ordenanza. Cuando el tipo no tiene respaldo suficiente se conserva la pregunta; no se rellena calle por defecto.

| ID / recibido | Resultado | Motivo o pregunta para revisión |
|---|---|---|
| 001 · 14 Provincias | 14 Provincias | El nombre y tipo calle coinciden con la referencia nacional; origen de 14 Provincias sin confirmar. Cotejo espacial municipal pendiente. |
| 002 · 2 de Abril | En consulta | ¿Qué entrada municipal confirma el tipo de vía y la grafía 2 de Abril? No se completa el nombre de una efeméride ni se presume el motivo de la denominación. |
| 003 · 25 de Mayo | 25 de Mayo | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |
| 004 · 9 de Julio | 9 de Julio | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |
| 005 · Aguila Mora | Águila Mora | p. 3 art. 3: la ordenanza cita calle Aguila Mora; se propone tilde de esdrújula sin atribuir especie. RAE-ACENTUACION. Uso publicado; no conformidad del plano. |
| 006 · Almafuerte | En consulta | ¿Qué documento identifica el tipo de vía y el referente de Almafuerte? El ejemplo preparado conservaba la grafía; no demuestra que sea un homenaje al escritor. |
| 007 · Almirante Brown | En consulta | ¿Qué documento identifica el tipo de vía y la denominación Almirante Brown? No expandir a un nombre completo sin una referencia municipal. |
| 008 · Alsina | En consulta | La referencia nacional contiene ALSINA como calle. ¿Qué documento municipal identifica su referente? No elegir entre personas con ese apellido por coincidencia biográfica. |
| 009 · Anisacate | En consulta | ¿Qué documento confirma grafía y tipo de vía de Anisacate? No cambiar a otra variante del topónimo ni atribuir el homenaje a una localidad sin respaldo. |
| 010 · Arrecifes | Arrecifes | Conservar la grafía recibida; las referencias nacionales coinciden en texto normalizado y tipo. Referente sin confirmar; identidad espacial y vigencia municipal pendientes. |

## Cierre de esta revisión

Las preguntas anteriores se entregan agrupadas al referente. Solicitar la entrada y plano del nomenclador (Anexo A de 920/2020 y sus modificaciones), el tipo de vía y, cuando corresponda, el texto de la ordenanza de denominación. No se enviaron mensajes a terceros.

Al obtener un documento, registrar su referencia publicable y revisar la relación entre vía y registro; cambiar una consulta a propuesta no genera conformidad. El supervisor registra por separado cualquier decisión municipal sobre el texto exacto.

Comprobación: `python scripts/validar.py`; `python scripts/auditar_referencias.py`; generación de entrega en carpeta nueva. Las consultas no entran al archivo de cambios aprobados.

El lote 01 se mantiene reservado a material de aprendizaje. Esta auditoría corrige el respaldo y las dudas de esos ejemplos; no se atribuye al estudiante como producción. Las cantidades de estados se obtienen de los CSV actuales.
