# Aprender con un caso: ¿qué hacemos con “Alsina”?

El plano contiene un rótulo que dice **Alsina**. Sabemos lo que está escrito; todavía no sabemos a quién o a qué alude la denominación municipal.

## Paso 1: separar observación de interpretación

| Afirmación | ¿Qué la sostiene? |
|---|---|
| El rótulo recibido dice Alsina | El CSV crudo y la posterior comprobación contra el dibujo |
| Debe decir el nombre completo de cierta persona | Todavía falta una fuente municipal |
| Hay que consultar a la autoridad | La ambigüedad del caso |

Una coincidencia encontrada en internet ayuda a formular una pregunta. No demuestra la intención de la denominación municipal.

## Paso 2: registrar una consulta útil

La fila de ejemplo conserva el ID y el nombre crudo. Los campos de propuesta se dejan vacíos:

```csv
id,nombre_crudo,nombre,tipo,homenaje,estado,nota,fuente
008,Alsina,,,,en_consulta,Confirmar el referente de la denominación y la grafía oficial mediante una fuente municipal,
```

La fila ilustra el formato; no hay que copiarla sobre todo un archivo. Una pregunta como “¿A quién refiere esta denominación y en qué documento se estableció?” permite una respuesta concreta. “No sé” no le dice al referente qué información falta.

## Paso 3: leer una fuente antes de proponer

Si la autoridad aporta una referencia, se registra su identificación publicable y se revisa la grafía. No copies documentos internos, firmas ni datos privados en el repositorio público. El supervisor custodia la evidencia que no pueda publicarse.

Si la fuente no llega, el caso sigue `en_consulta`. Ya hiciste un trabajo útil: detectaste y delimitaste una incertidumbre.

## Paso 4: validar y pedir revisión

Ejecutá **Callejero: Validar datos**. Un resultado correcto significa que la fila cumple las reglas del proyecto; no demuestra que una interpretación histórica sea verdadera. El PR permite revisar tanto la fila como tu razonamiento.

## Paso 5: distinguir las dos revisiones

El supervisor puede aceptar que tu trabajo está bien documentado e incorporar la consulta a `main`. Eso no aprueba una corrección de nombre. Una conformidad municipal posterior se registra en otro archivo, con el texto exacto y su referencia.

## Pequeño glosario

| Palabra | Qué significa aquí |
|---|---|
| Rótulo | Un texto visible en el dibujo |
| Handle | Identificador de una entidad CAD; una misma calle puede tener varios rótulos |
| Lote | Un archivo que reúne calles para organizar el trabajo |
| CSV | Tabla guardada como texto, con columnas separadas por comas |
| Fuente | Documento, referencia o criterio que respalda una afirmación |
| Propuesta | Nombre que se presenta a revisión, incluso si se conserva la grafía |
| Consulta | Pregunta explícita cuando falta evidencia |
| Validación | Comprobación automática de formato y coherencia |
| Rama | Lugar separado para trabajar sin modificar directamente `main` |
| Commit | Una versión guardada con un mensaje |
| Push | Envío de esos commits al repositorio |
| PR | Solicitud para que otra persona revise la contribución |
| Conformidad | Decisión municipal registrada sobre el nombre exacto |

**Ejercicio para conversar:** ¿por qué una consulta bien planteada puede ser mejor trabajo que un nombre completado por intuición? Mostrá qué evidencia te haría cambiar de consulta a propuesta.
