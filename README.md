# Callejero · pasantía de dos meses

Un proyecto educativo para revisar nombres de calles, documentar fuentes y entregar propuestas a la autoridad municipal. Dedicación: **una hora por día hábil durante dos meses calendario**, con un núcleo planificado de 40 horas.

Repositorio previsto: https://github.com/los-topos-cosmicos/callejero-yacanto

**Empezar por [EMPEZAR_AQUI.md](EMPEZAR_AQUI.md).** La localidad todavía debe confirmarse; el nombre del repositorio no constituye evidencia de procedencia.

## Qué hay y qué falta

La base recibida tiene **251 calles, 1.102 rótulos y 1.102 handles únicos**. Los CSV son consistentes entre sí. El lote 01 contiene seis ejemplos de conservación de nombre y cuatro consultas; los otros 241 registros siguen sin revisar. No hay conformidades municipales registradas: el archivo de cambios CAD aprobado empieza vacío.

Están incluidos el plan diario de 40 sesiones, la propuesta formal en español, los lotes, el visor, la validación, las pruebas, el informe de ejemplo y el procedimiento CAD. Se conservaron los CSV crudos del último paquete recibido, con sus huellas SHA-256.

Quedan pendientes la confirmación de localidad, la georreferenciación y la prueba en AutoCAD sobre una copia. Las coordenadas geográficas heredadas no se presentan como verificadas. El GeoJSON de entrega contiene atributos y geometrías nulas; el visor muestra coordenadas relativas del dibujo. Son puntos de referencia, **no ejes de calles**.

## Preparar el entorno

Requiere Python 3.12 o posterior. En macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-extraccion.txt
python scripts/validar.py
python -m unittest discover -s tests -v
```

En PowerShell, usar `py -3 -m venv .venv` y luego `.venv\Scripts\python.exe` en lugar de `python`; no hace falta cambiar la política de ejecución.

## Trabajo cotidiano

1. Leer [CONTRIBUIR.md](CONTRIBUIR.md) y la tarea de la semana.
2. Editar 5–10 filas del lote asignado, registrar fuente o pregunta.
3. Ejecutar `python scripts/validar.py` y abrir un Pull Request.
4. Revisar la devolución antes de continuar. `aprobada` no se escribe en un lote.

```bash
python scripts/construir.py
python scripts/previsualizar.py
python scripts/generar_entrega.py --salida build/entrega-01
python scripts/generar_propuesta.py
python -m http.server 8000 --directory web
```

Abrir http://localhost:8000 para consultar el visor. Usar una carpeta nueva para cada entrega; el generador se niega a sobrescribir una anterior. GitHub Actions repite la validación y deja archivos de revisión como artefactos, sin escribir ramas ni comentarios con permisos elevados.

## Dónde encontrar cada cosa

| Archivo o carpeta | Para qué sirve |
|---|---|
| `propuesta/propuesta_pasantia.pdf` | Documento formal para el docente y la autoridad |
| `docs/PLAN_40_HORAS.md` | Ocho bloques semanales y 40 sesiones |
| `docs/ROLES_Y_BENEFICIOS.md` | Qué gana y qué aporta cada participante |
| `docs/SUBIR_A_GITHUB.md` | Primer push y protección de `main` |
| `docs/REVISION_Y_LIMITACIONES.md` | Correcciones efectuadas y verificaciones pendientes |
| `ISSUES.md` | Diez tareas listas para abrir en GitHub |
| `datos/lotes/` | Trabajo del estudiante; lote 01 es ejemplo |
| `datos/crudo/` | Base preservada y manifiesto de integridad |
| `datos/conformidad.csv` | Decisiones documentadas sobre nombres exactos |
| `entrega/` | Rutina AutoLISP y procedimiento de prueba |
| `ejemplos/entrega/` | Informe y salidas del estado inicial, sin correcciones aprobadas |
| `scripts/extraer.py` | Nueva auditoría de un DXF, sin reemplazar la base |
| `web/` | Visor local y exportaciones reconstruibles |

No se incluyen DWG, DXF, imágenes del plano ni geometrías parcelarias. El repositorio de destino es público: revisar con la autoridad la difusión de los datos de rótulos antes de subir. La licencia MIT corresponde al código; no otorga derechos sobre los datos municipales. Ver [NOTICE.md](NOTICE.md).
