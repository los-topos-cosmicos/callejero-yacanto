# Revisión del lote 02 · IDs 011–020

Fecha de consulta: 2026-10-24. Esta revisión trabaja sobre los diez registros recibidos; no es un ejercicio ficticio ni una conformidad municipal. Se conservan IDs, nombres crudos y asociaciones a rótulos. La correspondencia del plano con la localidad sigue pendiente de confirmación institucional.

## Resultado y alcance

- Dos propuestas de corrección: `Av Jose Marrero` → `Av. José Marrero` y `Av, Virgen de los 3 Cerritos` → `Av. Virgen de los 3 Cerritos`.
- Cuatro propuestas de conservación: IDs 016, 017, 018 y 020. Conservar no implica haber certificado su denominación oficial.
- Cuatro consultas concretas: IDs 011, 012, 013 y 019.
- Ninguna conformidad nueva. Las dos correcciones afectan 13 rótulos recibidos (9 + 4); solo se exportan para simulación mientras no exista aprobación.

La revisión distingue tres clases de respaldo: uso escrito en una publicación municipal, criterio ortográfico y conservación explícita de lo recibido. No presenta esas clases como equivalentes a una ordenanza. El tipo avenida se lee del prefijo recibido; para los IDs sin tipo explícito se solicita documentación. El homenaje permanece sin confirmar; una coincidencia biográfica o turística no demuestra la intención de una denominación.

## Fuentes verificadas

**F1 · Turismo municipal, ficha LO DE JUANO.** [Dónde comer](https://www.villayacanto.tur.ar/dondecomer), apartado Dirección. El portal identifica a la Municipalidad como creadora y está enlazado desde [el sitio municipal](https://www.villayacanto.gob.ar/), sección Soy Turista. La dirección usa «Av. José Marrero esquina Maipú». Respalda el texto propuesto del ID 014; no determina a quién homenajea ni acredita la correspondencia de esta vía con los handles del DWG.

**F2 · Mapa turístico municipal.** [Página de descarga](https://www.villayacanto.tur.ar/mapa-turistico) y [PDF de una página](https://www.villayacanto.tur.ar/_files/ugd/e11905_0273f519a1344012aa82c122cd7b0dc1.pdf). Descargado y cotejado visualmente. En el casco céntrico figura la avenida Lanza Donatti con doble t; también figura la avenida José Marrero, aunque en ese rótulo no aparece la tilde. La ficha F1 aporta la forma acentuada.

El PDF identifica un sendero de la Virgen de los 3 Cerritos y un mirador de Jesús de los Linderos. Esos atractivos no prueban que las avenidas del inventario lleven oficialmente esos nombres. No se copia la tilde que el folleto agrega a Virgen ni se cambia 3 por Tres.

SHA-256 del PDF consultado: `9eac04c187b0703dfc11e3bdbed912c4aff4d0d3097d86aacd62decbdfb82f62`. Se registra para reconocer la versión si cambia la descarga; no es una firma de aprobación. No se incorpora una copia de la cartografía al repositorio.

**F3 · RAE-ASALE, abreviaturas.** [DPD, apéndice 2](https://www.rae.es/dpd/ayuda/abreviaturas), entrada de avenida. Permite justificar el punto de la abreviatura y leer el tipo del prefijo. En el ID 015 se propone sustituir únicamente la coma después de Av; se conserva la inicial y el resto del texto recibido. Es un criterio ortográfico publicable, no una fuente municipal de denominación.

**F4 · Agencia Córdoba Turismo, guía de senderos.** [Guía de senderos de Córdoba](https://cordobaturismo.gov.ar/wp-content/uploads/2024/09/Senderos-Turistico-2024.pdf), página 49 del PDF, ficha Calamuchita / Villa Yacanto / Sendero Jesús de los Linderos. Descarga comprobada y texto de la ficha revisado. Identifica un sendero y su destino; orienta la consulta del ID 019 sobre la tilde y la relación con la avenida. No se usa para dar por establecida esa relación.

**F5 · Inventario recibido.** [calles_crudo.csv](../../datos/crudo/calles_crudo.csv), IDs 011–020, y [etiquetas.csv](../../datos/crudo/etiquetas.csv). Aporta el texto base, el prefijo cuando existe y las cantidades de rótulos. En 016–018 se conserva la escritura por ese criterio limitado; no se afirma una corroboración externa que no se obtuvo.

## Decisión por registro

| ID | Decisión | Qué respalda la decisión / qué falta |
|---|---|---|
| 011 | Consulta | F5 no explicita tipo ni referente. Pedir documento municipal; no atribuir automáticamente el nombre a otra localidad. |
| 012 | Consulta | El texto recibido se mantiene en nombre_crudo. Falta documento que identifique tipo y denominación; no completar calle por defecto. |
| 013 | Consulta | Falta tipo y denominación documentados. No reemplazar el seudónimo recibido por un nombre civil. |
| 014 | Corregir punto y tilde | F1 acredita el uso municipal escrito; F2 corrobora avenida y apellido. Referente histórico pendiente. |
| 015 | Corregir solo la puntuación de Av | F3 y F5 sustentan la propuesta tipográfica. La grafía de un sendero en F2 no autoriza renombrar la avenida. |
| 016 | Conservar | F5 ya trae Av. Central con puntuación coherente. No hay fundamento reunido para expandir o cambiar el nombre. |
| 017 | Conservar | F5 ya trae Av. Costanera. No añadir un río ni atribuir referente. |
| 018 | Conservar | F5 ya trae Av. del Parque. No identificar un parque concreto sin respaldo. |
| 019 | Consulta | F2/F4 identifican un atractivo/sendero; falta documento que vincule la avenida con ese nombre y confirme la tilde. |
| 020 | Conservar doble t | F2 coincide con F5. No reducir Donatti a Donati por variantes en cartografía de terceros. |

## Preguntas agrupadas para el referente

1. Para IDs 011–013: aportar referencia de la denominación y el tipo de vía de cada registro. Si existe un nomenclador, indicar su versión y dónde figuran estos IDs o sus equivalencias.
2. Para ID 019: confirmar si la avenida corresponde a la denominación del atractivo Jesús de los Linderos y aportar su texto oficial.
3. Revisar las dos correcciones propuestas y las cuatro conservaciones. Para ID 015, decidir por documento si se mantiene el numeral 3; esta propuesta no lo cambia. Aceptar el PR solo incorpora trabajo de revisión; las conformidades se registran por separado con el texto exacto.

No se enviaron consultas ni se contactó a terceros durante esta revisión. Las preguntas quedan listas para que el referente gestione las respuestas.

## Comprobación reproducible

Ejecutar **Callejero: Validar datos**, **Callejero: Ejecutar pruebas** y **Callejero: Generar entrega**. En el paquete, comprobar que las correcciones de los IDs 014 y 015 suman 13 filas en propuestas_por_rotulo.csv, que los cuatro casos dudosos aparecen en consultas_pendientes.csv y que actualizaciones_aprobadas.csv no incorpora estas propuestas sin conformidad. Los resultados del inventario completo también incluyen los diez ejemplos previos.
