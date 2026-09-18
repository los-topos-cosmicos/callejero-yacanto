# Conocer el lugar antes de revisar los nombres

El proyecto tiene como referencia **Villa Yacanto, provincia de Córdoba, Argentina**.

**[Abrir Villa Yacanto en Google Maps](https://maps.app.goo.gl/7nQ2W2qGBmtEGNKU6)**

El coordinador compartió este enlace el 18 de septiembre de 2026. Se comprobó que redirige a la ficha de Villa Yacanto. La ubicación de esa ficha es aproximadamente **32,1057442° S, 64,7540869° O**. Es una referencia para orientarse; la cantidad de decimales no expresa precisión topográfica.

## Una exploración de cinco minutos

1. Abrí el enlace en otra pestaña del navegador.
2. Alejá la vista para reconocer Córdoba y acercala para ver la localidad.
3. Buscá un nombre del lote 01. Anotá qué aparece y de dónde sale la observación.
4. Si el plano, el inventario y Google Maps difieren, escribí una pregunta para el referente. Buscar evidencia y conservar la duda es parte del trabajo.

## Qué aporta esta referencia

| Referencia | Uso |
|---|---|
| Enlace de Google Maps | Ubicar Villa Yacanto y explorar su contexto |
| Nombres mostrados por Google Maps | Ayudar a investigar; no sustituyen una decisión municipal |
| Coordenadas del punto de la localidad | Abrir la vista cerca del lugar; no son un punto de control identificado en el DWG |
| Coordenadas X/Y de los rótulos | Posiciones heredadas del dibujo, con sistema de referencia por verificar |

La confirmación institucional de que el DWG corresponde a este lugar sigue registrada por separado en `config/proyecto.json`. Agregar este enlace no transforma ni valida las posiciones de las calles. El GeoJSON conserva sus geometrías nulas hasta completar la verificación espacial.

Los valores de referencia se conservan en `ubicacion_referencia` dentro de la configuración. Proceden del punto de la ficha (`!3d…!4d…` en la URL resuelta), no del centro de la cámara (`@…`) ni de una conversión de las coordenadas del plano.
