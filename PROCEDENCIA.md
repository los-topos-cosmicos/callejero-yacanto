# Procedencia y grado de verificación

Revisión del paquete: 18 de septiembre de 2026. Base utilizada: última revisión `callejero-municipal.zip` recibida dentro de `filespasantia(2).zip`. El repositorio se prepara bajo el nombre existente `callejero-yacanto`.

## Archivos fuente

| Fuente | SHA-256 | Qué se verificó en esta revisión |
|---|---|---|
| DWG municipal recibido | `eaf9842736b4419db24dff7f699927a6cbb0d5ca58bb3c71aabfea0bb2914c8b` | Se calculó la huella del archivo suministrado; no se abrió en AutoCAD |
| DXF declarado en el paquete anterior | `1573a3848d8e8b610a83eab553bf8fc8acd8917a1e98cc1661ef50a703e44246` | Huella heredada, no comprobada: no se dispone aquí del DXF correspondiente |
| Dos CSV de `datos/crudo/` | Ver `datos/crudo/manifest.json` | Conservados sin cambios y contrastados entre sí |

La conversión DWG→DXF mediante LibreDWG es un antecedente declarado en el material recibido. No se reprodujo durante esta revisión. Que los CSV tengan handles únicos no prueba por sí solo que todos correspondan al DWG original; debe cotejarse en una copia con el operador CAD.

## Lo comprobado en los CSV

- 251 IDs distintos de calle.
- 1.102 rótulos y 1.102 handles únicos.
- Correspondencia consistente entre cada rótulo, ID y nombre crudo.
- Recuento de rótulos por calle consistente con el inventario.
- 39 registros marcados fuera del recorte heredado.

Los nombres crudos proceden de una extracción previa que puede haber limpiado formato. Por eso la rutina exige que el texto actual de la entidad coincida exactamente; si no, se revisa manualmente. No se afirma que los CSV permitan reconstruir todo el contenido original del DWG.

## Reproducir una nueva auditoría DXF

```bash
python -m pip install -r requirements-extraccion.txt
python scripts/extraer.py /ruta/ejido.dxf --dwg /ruta/original.dwg --salida build/extraccion-01
```

El script usa `ezdxf`, preserva el texto original y el texto plano en columnas distintas, registra tipo, espacio, handle, coordenadas y versiones. Compara los handles con la base y señala faltantes o diferencias. No transforma coordenadas, no expande entidades anidadas en bloques y no reemplaza `datos/crudo/`, los IDs ni las conformidades. Una nueva base requiere revisión y migración explícita del supervisor.

El archivo DXF debe exportarse con una herramienta y versión registradas por el operador. Conservar ambos originales y sus hashes. La auditoría incluye un test con DXF sintético; esto no equivale a haber reextraído el plano real.

## Supuestos pendientes

1. **Localidad:** confirmar expresamente con la institución. El nombre del repositorio no resuelve esta verificación.
2. **CRS:** EPSG:22194 es una hipótesis heredada. Solicitar metadatos del dibujo y controles distribuidos; un punto aislado no certifica por sí solo datum, faja, unidades o posibles desplazamientos. Las latitudes y longitudes crudas se conservan como antecedentes, no se publican como geometría validada.
3. **Recorte:** la atribución previa de las 39 calles fuera de recorte a láminas de detalle no se pudo sostener con los CSV. Verificar el contenido espacial del DWG/DXF. El gráfico actual incluye todos los puntos de referencia sin ese supuesto.
4. **AutoCAD:** prueba real en copia pendiente. Revisar handles, texto plano, encoding, omisiones y deshacer.

La base catastral completa, el DWG/DXF, imágenes y polígonos de parcelas no forman parte de este repositorio. No se declara que el inventario sea el primero existente en la localidad: ese antecedente no está comprobado.
