# Evaluación del plan y cambios de esta versión

## Evaluación

La idea central es sólida: proponer correcciones trazables por handle y dejar la decisión en la institución reduce el alcance de intervención respecto de reemplazar todo el DWG. El valor educativo está en investigar, documentar incertidumbre, recibir revisión y entregar algo comprensible. El nuevo horario exige alcance flexible: dos meses a una hora por día hábil no son dos meses a jornada completa.

El paquete anterior mejoró varios controles, pero no justificaba afirmar que todo estaba resuelto. Se encontraron diferencias entre las explicaciones y lo que hacían los scripts. Esta versión trata los controles automáticos como apoyo a revisión humana, no como certificación del plano o de los nombres.

## Correcciones implementadas

| Hallazgo | Resultado en este paquete |
|---|---|
| El generador incluía propuestas sin conformidad en el TXT de aplicación | Solo nombres exactos con conformidad entran en el archivo aprobado. Las propuestas van a otro archivo que el LISP solo simula |
| Conformidad ligada únicamente al ID | Se exige ID, texto original y texto aprobado exactos, fecha válida y referencia; una modificación posterior invalida la conformidad |
| Cada exportador interpretaba los CSV por su cuenta | Lectura y validación comunes; el generador no copia un GeoJSON viejo |
| Cabeceras, IDs, separadores y códigos de formato ambiguos | Cabecera estricta, IDs exactos, formato CSV controlado y contrato de texto plano para CAD |
| Windows-1252 inferido solo por la página de códigos del dibujo | Rutina con lectura UTF-8 explícita, AutoCAD 2021+ y LISPSYS 1/2; auxiliar CP1252 separado y rechazado por la rutina |
| Reejecución, fallas de escritura y cancelación | Relectura tras entmod, reconocimiento de YA_ACTUALIZADO, registro único y aviso honesto de cambios parciales; pendiente ensayo real |
| Escritura de ramas y comentarios desde CI de PR | CI con contents:read, sin persistir credenciales; resultados como artefactos |
| Publicación descrita como desactivada pero ejecutable manualmente | Pages requiere ejecución manual en main y variable PUBLICAR_VISOR=true |
| Popup web interpretaba atributos como HTML | Visor con nodos DOM y textContent, sin interpolar datos en HTML |
| Coordenadas provisionales presentadas como mapa | Visor del dibujo; GeoJSON con geometría nula hasta verificación |
| Las 39 calles fuera del recorte quedaban excluidas o se atribuían a detalles sin evidencia | Se muestran todas y se mantiene la causa como pendiente |
| Extracción sobrescribía la base e infería coordenadas | Auditoría separada que preserva original/formato y compara handles; no migra IDs ni sobrescribe los lotes |
| Supuestos históricos en ejemplos y ausencia de fuente | Los seis ejemplos conservan grafía y declaran el referente pendiente; fuente/criterio explícito y cuatro consultas |
| Plan y nombre del repositorio inconsistentes | Dos meses calendario, 40 sesiones base y repositorio callejero-yacanto |

## Comprobaciones realizadas

Ver `VERIFICACION.md` para el resultado de ejecución de esta versión. Los tests modifican copias temporales y prueban errores relevantes, aprobaciones obsoletas, exclusión de propuestas, acentos, integridad de salidas y extracción de un DXF sintético.

El caso de acentos usa los **9 handles** que los CSV recibidos asignan a `Av Jose Marrero`. La afirmación anterior de 13 rótulos para ese nombre no coincide con estos archivos. El test es sintético: proponer `Av. José Marrero` allí no constituye aprobación municipal.

## Lo que sigue pendiente

- Confirmar localidad, titularidad y alcance de difusión del repositorio público.
- Contrastar CRS y posiciones; disponer de un punto ayuda, pero no prueba toda la georreferenciación.
- Verificar la correspondencia de handles y textos con el DWG y probar la rutina dentro de AutoCAD sobre una copia.
- Contar con una decisión institucional sobre cada corrección que se quiera aplicar.
- Configurar CODEOWNERS con usuario real y activar reglas de main después del primer push.
- Comprobar la ejecución de GitHub Actions en el repositorio remoto. El paquete no se subió automáticamente.

Las comprobaciones automáticas no autentican una firma, no validan historia local ni comprueban que una persona tenga competencia institucional. Un check verde no sustituye esos actos.
