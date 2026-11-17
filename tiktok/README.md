# TikTok Psiclín: sketches actuados con las comas

Videos cortos actuados con muñequitos propios de la marca: las dos comas del isotipo convertidas en personajes. Son situaciones cotidianas en las que la gente se reconoce, con humor suave y un cierre útil. Las voces se hacen en ElevenLabs con acento colombiano.

**Este archivo es la guía de producción.** Las métricas de cada video y los patrones que se van aprendiendo están en [BITACORA.md](BITACORA.md).

## Personajes y voces (no cambiarlos sin aprobación de Santy)

| Personaje | Color | Accesorio | Voz ElevenLabs (voice_id) | Rol |
|---|---|---|---|---|
| Tú (Coral) | coral #FF8C7A | — | Mariana, la amiga paisa (`YyzMdrXIPdg4iUnQfJ1D`) | La protagonista: le pasa lo que le pasa a la audiencia |
| La psicóloga | cielo #7EC8E3 | gafas | Claudia Isabel (`heUagVbSyc7SphaYWFT3`) | Da el consejo práctico, cálido, nunca regaña |
| Tu cerebro | rosa #FFC2D1 | — | Yohan Melguizo (`M67yD2NH1lnnCUDjlTGP`) | El sobrepensar, el drama y los pensamientos intrusivos en clave de humor |
| Mateo | verde #7EC8A0 | — | Juanpa (`eiBGX6sNyy93U47Mf8jI`) | Protagonista hombre |
| Andrés | arena #F4B266 | gorra | Alejandro, enérgico (`GXPbe9YHkbXZEa0DBAFA`) | El amigo |
| Tu amiga | arena #F4B266 | — | Fernanda (`jTXAEv4RIGK9R4kfx1by`) | La amiga |
| El psicólogo de película | café #8A7A6A | barba | Juan Pablo, voz grave (`JmwppWx5vSX4FtbIik4Z`) | El cliché que desmentimos |

- **Modelo de voz:** `eleven_v4`.
- **Un llamado por personaje y por video:** cada frase va en un párrafo, con etiquetas de emoción en inglés al inicio (por ejemplo `[sighs, sad]` o `[excited]`). No se leen en voz alta.
- **Dejar las 2 tomas.**
- **Nunca repetir un llamado que falló.**

## Estructura de un sketch (25–35 s)

1. **Título fijo arriba.** Es el gancho, en menos de 7 palabras: «Tu cerebro a las 3 a. m.».
2. **Situación reconocible en los primeros 2 s.** Un personaje habla de una vez, sin intro.
3. **Giro o remate gracioso.** Puede ser lo que no se dijo, el cerebro que interrumpe o la expectativa contra la realidad.
4. **Consejo breve de la psicóloga, o un gesto humano entre amigos.** Debe ser práctico y sin diagnosticar.
5. **Tarjeta de cierre (3 s):** la idea en una frase más una nota en Caveat.
6. **Cierre de marca (2,6 s):** las comas, el isotipo, «Psicología que te escucha.» y «Escríbenos · link en la bio».

## Reglas de contenido (no negociables)

- El humor va sobre **situaciones**, nunca sobre trastornos ni personas. Nada de «estoy tan OCD», «bipolar» o «depre» como chiste.
- No diagnosticar ni prometer resultados. Si el tema puede ser un síntoma persistente, la tarjeta final invita a hablarlo con un profesional.
- Crisis, autolesión o suicidio: no se tratan en clave de humor. Si alguna vez se tocan, va la Línea 106 y la línea de Medellín (604) 444 44 48, sin detalles de métodos.
- Sin precios, horarios ni promociones que Santy no haya confirmado.
- Solo la marca Psiclín. Nada dirigido a psicólogos, porque eso es de Psiclín Consultorios.
- Un psicólogo de la clínica valida el guion antes de publicar.
- Fechas y tendencias: se usan las amables (Black Friday, fin de año, Wrapped, alumbrados, novenas). Se evitan tragedias, política y fechas serias en clave de humor; por ejemplo, el 25 de noviembre no lleva humor.

## Cómo producir

El código está en `engine/`:

- `chars.py`: los personajes.
- `skit.py`: el motor, que hace la boca sincronizada con la voz, el parpadeo, los escenarios y los subtítulos.
- `skits.py`: los guiones del lote 1, que sirven de plantilla.
- `audio.py`: corta cada toma en frases.

Pasos para producir un video:

1. Generar las voces en ElevenLabs y descargarlas a `audio/<sketch>_<personaje>_<a|b>.mp3`.
2. Verificar los cortes de cada frase con faster-whisper (modelo `small`, español, `word_timestamps=True`) y poner los tiempos en `skits.py`.
3. Correr `python3 skits.py preview <ID>`, mirar los cuadros y corregir cualquier solape.
4. Correr `python3 skits.py render <ID>`.
5. Subir el MP4 a `tiktok/videos/` y programarlo en Metricool. Solo con aprobación.

Necesita Playwright con Chrome (`/usr/bin/google-chrome`), ffmpeg y las fuentes de `../src/fonts`. El motor toma las fuentes de `/home/claude/pack/src`; si no existen, se copian desde `../src` del repo.

## Métricas que leemos (TikTok, vía Metricool)

- **Alcance y vistas:** vistas, alcance y la tasa de visualización completa.
- **Retención:** tiempo medio de visualización y su porcentaje sobre la duración del video.
- **Interacción:** me gusta, comentarios, compartidos y guardados, cada uno dividido por las vistas.
- **Crecimiento:** seguidores ganados y visitas al perfil.
- **Negocio:** conversaciones de WhatsApp que mencionen TikTok. Este dato lo da Santy, cuando lo tenga.

Metas iniciales (orientativas, se ajustan con datos):

- Vista completa > 25 %.
- Compartidos/vistas > 1 %.
- Guardados/vistas > 0,8 %.

Con 3 videos por semana, **una semana sirve para descartar; para declarar un patrón se necesitan 2 o 3 semanas.**
