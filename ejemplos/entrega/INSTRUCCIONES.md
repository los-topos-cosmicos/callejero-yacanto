# Procedimiento CAD para el operador municipal

**Estado de la rutina: no ejecutada en AutoCAD durante la preparación de este paquete.** Los tests de Python y la revisión estática del LISP no sustituyen la prueba dentro de AutoCAD. El objetivo es modificar textos puntuales conservando el DWG como archivo de trabajo del operador, sin convertir todo el dibujo de regreso desde DXF.

## Archivos y autorización

- `actualizaciones_aprobadas_utf8.txt`: solo cambios con conformidad sobre el nombre exacto. Puede estar vacío; en el ejemplo inicial no hay cambios autorizados.
- `propuestas_simulacion_utf8.txt`: propuestas de revisión. Su cabecera obliga a la rutina a permitir únicamente simulación.
- `actualizaciones_aprobadas_cp1252.txt`: auxiliar para un procedimiento externo que requiera Windows-1252. **Su cabecera impide seleccionarlo en la rutina suministrada**, que lee UTF-8 explícito.
- `actualizaciones_aprobadas.csv`: versión legible para cotejar ID, handle y texto.
- `actualizar_calles.lsp`: comando `ACTUALIZAR_CALLES`.
- `manifest.json`: huellas de insumos y archivos de salida. No es una firma digital de aprobación.

La versión suministrada requiere AutoCAD 2021 o posterior y `LISPSYS` 1 o 2. Un cambio de LISPSYS requiere reiniciar AutoCAD. La codificación declarada en el DWG no determina por sí sola cómo AutoLISP abre un TXT: se usa `(open ruta "r" "utf8")` para evitar depender de la página de códigos del sistema. No se ofrece aquí una rutina validada para versiones anteriores.

## Prueba en una copia

1. Conservar el original y su copia de respaldo fuera del repositorio. Verificar con el responsable que el DWG es el mismo del que se extrajeron los rótulos; cotejar nombre, SHA-256, capa y muestras de handles. La rutina no calcula el hash del DWG abierto.
2. Crear una copia de trabajo identificable. Cerrar otros comandos de AutoCAD. Revisar que UNDO esté habilitado.
3. Cargar el LISP mediante APPLOAD siguiendo la política de rutas confiables de la oficina. No desactivar controles de carga de la organización.
4. Ejecutar `ACTUALIZAR_CALLES`, elegir el TXT **UTF-8** y pulsar Enter para **Simular**.
5. Leer el registro que queda junto al TXT (`.log`, `.1.log`, etc., sin sobrescribir registros anteriores). Revisar textos, cantidades, rótulos faltantes, diferencias y entidades con formato.
6. Para ensayar escritura se necesita un archivo de cambios con conformidades reales o un caso de prueba sintético preparado por el supervisor, claramente separado del expediente municipal. La rutina solo permite Aplicar con cabecera APROBADAS y tras confirmar que es una copia de prueba.
7. En la copia, probar **Aplicar** y revisar visualmente todos los cambios del ensayo, incluidos acentos. Volver a simular: debe informar YA_ACTUALIZADO. Usar una vez U y verificar que revierte el grupo completo. Probar Escape en un ensayo separado: puede dejar cambios parciales dentro del grupo; no guardar y verificar el deshacer.
8. Registrar versión de AutoCAD, LISPSYS, hash de insumos, resultados y operador en `ACTA_PRUEBA_CAD.md` (incluido en el paquete generado), manteniendo firmas o identificación privada fuera del repositorio.

## Comportamiento y límites

La lectura del archivo completo valida cabecera, número de campos, duplicados y texto plano antes de modificar. Se resuelven handles y se comprueban tipo TEXT/MTEXT, capa exacta `NOMBRE CALLES`, espacio modelo, capa desbloqueada y texto esperado. Se omiten códigos de formato, campos y MTEXT fragmentado para revisión manual; el código DXF 3 indica fragmentos, no toda posible forma de formato.

Si una fila presenta una discrepancia con el dibujo, **Aplicar aborta antes de la primera escritura**. No modificar el TXT a mano para saltarla: revisar el origen y regenerar el paquete. Los textos que ya coinciden con el resultado se registran como YA_ACTUALIZADO.

Cada `entmod` se comprueba mediante su retorno y relectura. Si falla durante la escritura, se detiene el resto: pueden existir cambios parciales anteriores. La rutina cierra el grupo UNDO y los archivos, pero no promete transacción atómica ni recuperación de fallas del proceso de AutoCAD. El operador revisa y deshace antes de continuar. Nunca se guarda el DWG automáticamente.

Solo después de documentar la prueba en copia, de confirmar la correspondencia de handles y de contar con conformidad institucional, el responsable decide el procedimiento sobre su archivo oficial. Esta pasantía no exige que ese paso ocurra durante los dos meses.

## Referencias técnicas

- [Autodesk: lectura de archivos, Unicode y LISPSYS](https://help.autodesk.com/cloudhelp/2025/ENU/AutoCAD-AutoLISP-Reference/files/GUID-089A323F-21FF-4337-99A9-375758E23BA4.htm).
- [Autodesk: estructura DXF de MTEXT](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-DXF/files/GUID-5E5DB93B-F8D3-4433-ADF7-E92E250D2BAB.htm).
- [Autodesk: command-s dentro de manejadores de error](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-AutoLISP-Reference/files/GUID-5C9DC003-3DD2-4770-95E7-7E19A4EE19A1.htm).
