# Ver qué cambió en un Pull Request

Un PR es un pedido de revisión. Su imagen ayuda a conversar sobre el trabajo; el supervisor sigue leyendo las filas, las fuentes y las preguntas.

## Para el estudiante

1. Validá y subí el trabajo desde Codespaces.
2. Abrí el PR y esperá los controles de **Validar callejero**.
3. Leé el comentario **Vista de la revisión**. Incluye la versión del commit y un enlace a los controles.
4. Si se pide una corrección, seguí trabajando en la misma rama y hacé otro commit y push.

| Marca | Qué significa |
|---|---|
| Círculo naranja | Esa fila o su conformidad cambió respecto de la base del PR |
| Punto verde | Propuesta con fuente |
| Punto ámbar | Pregunta en consulta |
| Punto azul | Nombre con conformidad municipal registrada |
| Punto gris | Todavía sin revisar |

Un cambio de nota o fuente también se resalta. Reordenar filas o moverlas de lote no se cuenta como una revisión nueva. Las barras muestran el inventario completo, incluidos los ejemplos preparados. El gráfico incluye las 39 calles fuera del recorte anterior y usa coordenadas del dibujo.

Si la ejecución falla, el comentario reemplaza la imagen anterior por una indicación para revisar el error. **Checks** es la referencia para saber qué controles pasaron. Un check correcto no demuestra que un dato histórico sea verdadero ni aprueba un cambio municipal.

## Para el supervisor

- El workflow `validar.yml` ejecuta código propuesto con `contents: read`, conserva el check **validar** y sube un PNG como artefacto.
- `previsualizar.yml` se ejecuta mediante `workflow_run`, usando su definición y el publicador de la rama principal. No instala ni ejecuta scripts del PR con permisos de escritura.
- El publicador acepta únicamente un archivo `avance.png` dentro del ZIP, limita tamaño y dimensiones y comprueba su estructura y CRC. No extrae archivos ni ejecuta su contenido.
- Obtiene el número del PR y el SHA desde GitHub. Comprueba que el PR siga abierto, apunte a la rama principal y conserve esa versión. Los forks reciben validación y artefactos, sin publicación automática de comentarios.
- Las imágenes se agregan a `ci-previews`; se conservan las de otros PR y se enlazan por commit inmutable. El código y los datos de `main` no se escriben desde este publicador.
- Si una política de la organización bloquea escritura o comentarios, la validación y los artefactos siguen disponibles. No se necesita un token personal ni dar acceso Admin al estudiante.

La activación ocurre después de incorporar estos workflows a `main`: el primer PR que los agrega puede no recibir comentario. Después, abrí un PR de práctica con una consulta, verificá imagen y versión, provocá un error de formato temporal y comprobá el aviso. Corregí el error antes de incorporar ese PR. No se declara esta prueba remota realizada en la preparación del paquete.

La selección manual `python scripts/previsualizar.py --destacar lote-02.csv` resalta todo un lote y lo etiqueta como tal. En Actions se usa `--base` con el SHA de base para calcular las filas que cambiaron realmente.

Referencia técnica: [eventos workflow_run y uso de artefactos entre workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run).
