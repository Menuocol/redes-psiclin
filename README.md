# Psiclín · Calendario de Instagram (16 nov 2026 – 3 ene 2027)

Contenido listo para programar en Metricool. Basado en el Manual Maestro 360° de Psiclín.

## Qué hay aquí

- `posts/AAAA-MM-DD_PXX/NN.png`: 36 publicaciones (88 imágenes de 1080×1350). Un carrusel es una carpeta con varias imágenes en orden.
- `stories/AAAA-MM-DD/NN_tipo.png`: 112 historias (1080×1920), en orden de publicación por día.
- `calendario_posts.csv`: fecha, hora, caption con hashtags, texto alternativo, imágenes y pendientes de cada post.
- `calendario_historias.csv`: historias por día y el sticker que hay que agregar en la app.
- `manifest.json`: lo mismo en JSON, para programar en Metricool de forma automática.
- `index.html`: galería para revisar y aprobar todo de un vistazo (sirve con GitHub Pages).
- `src/`: el generador (plantillas HTML y fuentes de la marca) por si hay que cambiar un texto y volver a exportar.

## Cómo se programa

1. Las imágenes tienen que estar en una URL pública para que Metricool las tome: repo público (`raw.githubusercontent.com/...`) o GitHub Pages.
2. La marca "Psiclinmed" en Metricool tiene que tener Instagram (@psiclinmed) conectado.
3. Se programa semana por semana, solo lo aprobado y con la validación clínica de un psicólogo.

## Lo que no se puede programar

- **Historias con sticker** (encuesta, deslizador, caja de preguntas, enlace): la API de Instagram no agrega stickers. Esas se publican a mano a la hora indicada, o con la notificación al celular de Metricool. La columna "sticker a agregar en la app" dice cuál va.
- **Audio en tendencia** (por ejemplo "It's Time"): se agrega en la app de Instagram, no desde Metricool.

## Pendientes antes de publicar

- P21 (11 dic): reemplazar la foto por la del vasito real de la sala de espera.
- P33 (29 dic): opcional, agregar la foto real del equipo (con consentimiento de imagen).
- Confirmar con un psicólogo de la clínica todos los posts de salud antes de programarlos.

## Fotos

Las fotos de ambiente vienen de Unsplash (licencia libre con uso comercial). Ninguna persona de banco de imágenes aparece presentada como paciente ni como parte del equipo.
