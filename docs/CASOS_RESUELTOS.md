# Tres casos resueltos de práctica

**Todos los nombres, referencias e IDs de esta página son ficticios.** No son fuentes sobre Villa Yacanto y no deben copiarse a `datos/lotes/`. Leé cada fuente suministrada y después compará el resultado.

## 1 · Conservar una grafía

**Registro de práctica:** P01, Los Aromos. **Fuente didáctica F1:** «El inventario de esta actividad identifica la vía como calle Los Aromos; no informa el origen del nombre».

La fuente permite conservar el texto y clasificar la vía como calle. No demuestra qué conmemora. La clasificación se deja `sin_confirmar`.

```csv
id,nombre_crudo,nombre,tipo,homenaje,estado,nota,fuente
P01,Los Aromos,Los Aromos,calle,sin_confirmar,propuesta,Se conserva la grafía; origen del nombre sin confirmar.,Fuente didáctica F1 de esta actividad ficticia
```

## 2 · Proponer una corrección documentada

**Registro de práctica:** P02, Rio Claro. **Fuente didáctica F2:** «Artículo 1: denomínase calle Río Claro a la vía identificada como P02 en esta actividad». No identifica un homenaje.

La fuente sostiene el acento y el tipo. Proponerlo no equivale a que el municipio haya aceptado una modificación del plano real.

```csv
id,nombre_crudo,nombre,tipo,homenaje,estado,nota,fuente
P02,Rio Claro,Río Claro,calle,sin_confirmar,propuesta,Se agrega la tilde según el artículo suministrado.,Fuente didáctica F2 artículo 1 de esta actividad ficticia
```

## 3 · Consultar cuando la evidencia no alcanza

**Registro de práctica:** P03, Rivera. **Material suministrado F3:** una biografía de una persona apellidada Rivera; no menciona esta calle ni una decisión municipal.

La coincidencia no permite completar un nombre ni determinar el homenaje. La consulta mantiene vacío el nombre propuesto. Las comillas protegen la coma dentro de la pregunta.

```csv
id,nombre_crudo,nombre,tipo,homenaje,estado,nota,fuente
P03,Rivera,,,,en_consulta,"¿Cuál es la grafía oficial, y qué documento identifica el referente?",Fuente didáctica F3 insuficiente para establecer la denominación
```

## Una revisión completa

Para el caso 2, el estudiante explica en su PR: «Revisé P02. Propongo Río Claro porque F2 artículo 1 usa esa grafía. No identifiqué el homenaje».

El supervisor comenta: «La fuente respalda la tilde. Dejá el homenaje sin confirmar y explicitá el artículo». El estudiante corrige la referencia, valida desde el menú y sube otro commit a la misma rama. El supervisor revisa el razonamiento. Incorporar ese trabajo no agrega una conformidad municipal.

**Para conversar:** ¿qué documento faltaría en el caso 3? ¿Qué cambiaría si F2 no identificara la misma vía? Compará tus respuestas con el supervisor antes de trabajar sin ayuda.
