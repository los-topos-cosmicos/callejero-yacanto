### PROPUESTA DE PASANTÍA EDUCATIVA · PARA REVISIÓN INSTITUCIONAL

# Un callejero verificable,
un aprendizaje concreto

Organización y revisión de nombres de calles a partir de un plano municipal. Duración: dos meses calendario; dedicación: una hora por día hábil.

Modalidad: GitHub Codespaces desde el navegador. El entorno prepara Python, dependencias y herramientas automáticamente en GitHub. El estudiante no instala ni configura programas en su computadora.

| Dato institucional | Referencia / datos por completar |
| --- | --- |
| Localidad de referencia | Villa Yacanto, Córdoba, Argentina |
| Institución | Por completar |
| Estudiante | Por completar |
| Docente y autoridad referente | Por completar |
| Supervisor técnico | Por completar |
| Inicio / cierre | Por acordar / Por acordar |

Ubicación compartida por el coordinador: https://maps.app.goo.gl/7nQ2W2qGBmtEGNKU6

## Propósito

Producir un inventario consultable de nombres de calles, propuestas de corrección respaldadas y un registro de dudas para decisión municipal. El estudiante trabaja con datos y herramientas reproducibles; la autoridad conserva la decisión sobre el registro oficial.

La base recibida contiene 251 nombres agrupados y 1.102 rótulos con identificador de entidad. Estas cantidades se verifican en los CSV. Todavía no se ha comprobado, en AutoCAD, la correspondencia completa con el DWG original.

## Resultado mínimo comprometido

Un repositorio ordenado, un subconjunto revisado con fuentes, consultas explícitas, un informe final reproducible y una presentación. Revisar las 251 calles es una meta ampliada: no se promete cerrar todos los casos ni modificar el plano durante la pasantía.

### VALOR PARA CADA PARTICIPANTE

# Qué gana cada parte

| Participante | Beneficio concreto | Aporte requerido |
| --- | --- | --- |
| Estudiante | Aprende CSV, Git, revisión de datos, pruebas y comunicación. Obtiene un trabajo demostrable con historial. | Una hora por día hábil; registrar decisiones y pedir ayuda cuando falte evidencia. |
| Municipalidad | Recibe un inventario reutilizable, inconsistencias identificadas y correcciones trazables para evaluar. | Confirmar alcance, permitir uso de los datos y responder un conjunto acotado de consultas. |
| Docente / autoridad | Evalúa aprendizaje con evidencia y recibe una propuesta que puede aceptar parcialmente. | Separar evaluación pedagógica de conformidad municipal; designar quién decide cada cuestión. |
| Supervisor técnico | Dispone de una estructura de mentoría y revisión con avances observables. | Preparar el acceso a Codespaces, revisar PR y mantener aprobaciones y procedimientos CAD. |
| Comunidad | Puede beneficiarse de información más clara si la autoridad la valida y decide publicarla. | No se promete impacto inmediato sobre servicios, catastros o domicilios oficiales. |

## Una persona puede cumplir dos roles

Si el docente es también la autoridad municipal, se registran por separado la devolución educativa y la decisión institucional. Una buena calificación no aprueba automáticamente una corrección de nombre.

## Carga de acompañamiento propuesta

Docente/referente: 20–30 minutos semanales, con preguntas agrupadas. Supervisor: preparación inicial y 30–45 minutos semanales de revisión, ajustables según necesidad. Son aportes de adultos, fuera de las 40 horas base del estudiante.

### PLAN DE TRABAJO

# Dos meses, una hora al día

Se planifican 40 sesiones de una hora como núcleo. Dos meses calendario no equivalen siempre a ocho semanas: al fijar fechas se descuentan feriados, recesos y ausencias. Los días adicionales son margen para ajustes; si hay menos de 40 días se reduce el volumen de calles.

| Bloque | Horas | Trabajo y evidencia |
| --- | --- | --- |
| Semana 1 | 5 | Codespaces en el navegador, fuentes, lote 01 y primer PR de práctica. |
| Semanas 2–3 | 10 | Lotes pequeños; documentar fuentes, consultas y tiempos reales. Ajustar la meta al cierre de la semana 3. |
| Semanas 4–6 | 15 | Revisar nuevos lotes al ritmo observado; responder revisiones y mejorar una herramienta pequeña. |
| Semana 7 | 5 | Consistencia de nombres, fuentes y estados; resolver consultas priorizadas. |
| Semana 8 | 5 | Generar informe, ensayar presentación, entregar resultados y próximos pasos. |

## Cada sesión de 60 minutos

10 min: leer la tarea y la devolución. 40 min: trabajar en un caso acotado. 10 min: validar, guardar el avance y registrar la duda o el siguiente paso. Una sesión termina aunque el caso siga abierto.

## Volumen adaptable

Los lotes existentes son contenedores de datos, no cuotas diarias. Se trabaja en grupos de 5–10 calles y se divide cualquier lote grande. El lote 01 ya contiene ejemplos: no se cuenta como producción del estudiante. Los casos sin evidencia pasan a consulta sin consumir varios días en una búsqueda incierta.

## Criterio de éxito

Vale más un conjunto menor, verificable y bien documentado que completar 251 nombres por suposición. La aplicación al DWG y la publicación geográfica son actividades condicionales a cargo de personal competente.

### MÉTODO, ALCANCE Y ENTREGA

# Un proceso revisable

El estudiante registra una propuesta o una consulta en un CSV. Un Pull Request permite revisar su razonamiento y ejecutar controles. Solo el supervisor incorpora una conformidad documentada sobre el nombre exacto aceptado por la autoridad.

| Entregable | Uso |
| --- | --- |
| Inventario CSV y visor en Codespaces | Buscar nombres, consultar estados y leer fuentes. |
| Informe PDF + consultas CSV | Revisar resultados, responder dudas y registrar decisiones. |
| Rutina LISP + archivos de cambios | Simular o probar cambios aprobados sobre una copia; nunca convertir de regreso todo el plano. |
| GeoJSON de atributos | Estructura para futura integración SIG; geometría nula hasta verificar las posiciones. |
| Código, pruebas y procedencia | Reproducir validación, exportaciones y una nueva auditoría de extracción DXF. |

## Limitaciones que siguen abiertas

| Tema | Verificación necesaria |
| --- | --- |
| Plano y localidad | La referencia compartida es Villa Yacanto. El referente confirma que el plano y su alcance corresponden a esa localidad. |
| Coordenadas | Documentación del CRS y contraste con controles distribuidos. La ficha de Google Maps ubica la localidad, pero no es un punto de control identificado en el plano. |
| 39 calles fuera del recorte | Revisar su ubicación y el criterio del recorte. No se atribuyen automáticamente a láminas de detalle. |
| Rutina CAD | Probar en AutoCAD real, en copia, acentos, omisiones, reejecución y deshacer. Esta prueba aún no se realizó. |

El repositorio es público. No incluye el DWG, imágenes OLE ni una base parcelaria. Incluye datos de rótulos y coordenadas heredadas; corresponde acordar su difusión antes de subirlos. Los originales, firmas y documentación interna se conservan por separado.

### EVALUACIÓN Y ACUERDO

# Qué se pide aprobar

Se solicita acordar el alcance educativo y operativo de la pasantía; la aceptación de correcciones concretas será una decisión posterior, documentada por separado.

| Dimensión | Peso | Evidencia |
| --- | --- | --- |
| Trazabilidad y fuentes | 30% | Cada propuesta explica su criterio; las hipótesis están señaladas. |
| Juicio ante la incertidumbre | 25% | Preguntas concretas y decisión de no inventar información. |
| Trabajo con revisión | 20% | PR comprensibles, respuesta a comentarios y correcciones. |
| Aprendizaje técnico | 15% | Uso de validación y una mejora pequeña explicada y probada. |
| Comunicación y cierre | 10% | Informe, presentación y próximos pasos claros. |

La velocidad, la cantidad total de calles y el porcentaje de pruebas que pasan al primer intento son datos de acompañamiento, no medidas automáticas de mérito.

## Acuerdos antes de iniciar

1. Completar nombres, fechas y calendario hábil.
2. Confirmar localidad, alcance y difusión de los datos del repositorio público.
3. Nombrar referente y supervisor; acordar revisión semanal breve.
4. Solicitar documentación del sistema de coordenadas y puntos de control disponibles.
5. Acordar quién responde consultas y quién puede dar conformidad sobre nombres.
6. Reservar al operador CAD la prueba en copia y cualquier intervención institucional.
7. Comprobar el acceso del estudiante a Codespaces antes de la primera sesión.

## Si no hay conformidad al finalizar

Se entrega el inventario, las propuestas y las preguntas pendientes, con sus limitaciones. El aprendizaje y la documentación siguen siendo resultados válidos. No se aplica ninguna propuesta pendiente al archivo oficial.

Lugar y fecha: ______________________________________________
Institución / docente referente: _________________________________
Supervisor: __________________ Estudiante: ___________________
Observaciones y aceptación del alcance: ________________________
