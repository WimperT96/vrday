# 04 · Medios (imágenes y videos)

Lista completa archivo por archivo: [`anexos/inventario-medios.csv`](anexos/inventario-medios.csv) (página · uso · archivo nuevo · estado · URL original).

## 1. Estado general

| | Cantidad |
|---|---|
| Archivos únicos referenciados por el sitio actual | 201 (imágenes + 1 video MP4) |
| Descargados correctamente | **187** (≈ 43 MB) → `referencias/originales/` (ruta original) y `medios/` (ruta nueva) |
| Faltantes en el servidor (404) | **14**: 11 → placeholders `.svg` en `medios/heredadas/`; 3 eran de las fichas demo descartadas |
| Videos de YouTube | 11 embebidos, **todos disponibles** + 3 reproductores sin ID en VRD 2021 |
| Otros embebidos | 1 modelo 3D Sketchfab (Arte en cuarentena), 1 juego itch.io (Knockout) |

**Dato importante:** el HTML actual apunta a `virtualrealityday.utpl.edu.ec/wp-content/uploads/…`, dominio que **ya devuelve 404** (servidor Azure Application Gateway; verificado también con un navegador normal el 30-sep-2026). Es decir, **el sitio publicado hoy se ve prácticamente sin imágenes**. Los archivos se recuperaron desde `vrdaylatam.org/wp-content/uploads/…`, que sí responde.

## 2. Organización nueva (`medios/`)

| Carpeta | Contenido | Archivos |
|---|---|---|
| `marca/` | logo | 1 |
| `fondos/` | fondo azul general, cabecera 2023, cabecera 2020 | 3 |
| `banderas/` | 8 países | 8 |
| `patrocinadores/` | 5 logos del pie | 5 |
| `inicio/` | `slider/` (5), `estadisticas/` (3), `actividades/` (5), mapa | 14 |
| `ponentes/2023/`, `2021/`, `2020/` | fotos con nombre del ponente (`aura-forero.png`) | 40 + 19 + 12 |
| `memorias/2019 … 2022/` | galerías numeradas `01.jpg, 02.jpg…` (+ `00-afiche`, `00-portada`, `08-ganadores`) | 42 |
| una carpeta por página | `acerca-de/`, `plataforma-inmersiva/`, `stands-virtuales/`, `arte-en-cuarentena/`, `juego-knockout/`, `juego-cuidemonos/`, `red-aprendizaje-inmersivo/`, `agenda-2020/`, `acerca-de-vrd-anterior/` | — |
| `heredadas/` | placeholders de páginas heredadas | 11 |

Reglas de nombres: minúsculas, sin tildes ni espacios, guiones. Galerías numeradas con dos dígitos para mantener el orden.

## 3. Placeholders

Todos los faltantes pertenecen a páginas **heredadas y ocultas** (`/realidad-aumentada/`, `/inicio-aries/`, `/acordeon/`): eran imágenes de demostración del tema Kallyas que ya no existen.

| Placeholder | Uso |
|---|---|
| `heredadas/inicio-aries/banner.svg` | Banner de líneas de investigación |
| `heredadas/realidad-aumentada/que-es-ra.svg` | Fondo "¿Qué es RA?" |
| `heredadas/realidad-aumentada/app-generica.svg` | Tarjetas de apps / artículos |
| `heredadas/realidad-aumentada/app-estadistica.svg` | App Estadística |
| `heredadas/realidad-aumentada/fondo-virtopsia.svg` | Fondo bloque Virtopsia |
| `heredadas/realidad-aumentada/equipo/*.svg` (6) | Fotos del equipo del proyecto |

Formato del placeholder: SVG 1200×800 con el degradé de marca, borde punteado y la palabra PLACEHOLDER + descripción. Para reemplazarlo: guardar la imagen definitiva en la misma carpeta y cambiar la ruta (extensión) en el YAML.

**Placeholders de contenido** (no de imagen) — ver `06-problemas-de-contenido.md`: 3 videos vacíos de VRD 2021, botón "Descargar manuales", enlaces "Videotutorial" e "Instructivo", 16 reseñas de ponentes vacías (9 de 2023, 7 de 2020).

## 4. Optimización ✅ (26-oct-2026)

Hecha con `python referencias/herramientas/optimizar_medios.py --aplicar` (sin `--aplicar` solo simula):
195 imágenes PNG/JPG pasaron a WebP (38,9 MB → 6,4 MB), con lado mayor máximo según el uso
(ponentes y logos 600 px, banderas 160, íconos 256, fondos 2560, resto 1600) y conservando la
transparencia. Las rutas del contenido se actualizaron solas. Los medios sin uso se movieron a
`referencias/medios-sin-uso/` y los originales de la migración siguen en `referencias/originales/`.
El sitio exportado pasó de ~45 MB a 10,4 MB. Volver a ejecutar el script cuando se agreguen imágenes nuevas.

Tabla original del diagnóstico (referencia):

| Problema | Ejemplos | Acción |
|---|---|---|
| Imágenes gigantes | `fondos/fondo-general-azul.png` 6092×2670 · `acerca-de/cabecera.png` 5938×2384 (2,5 MB) · `patrocinadores/cop.png` 4948×1895 | Redimensionar a máx. 2560 px y convertir a WebP/AVIF |
| Fotos de ponentes de hasta 2560 px para mostrarse a ~300 px | `ponentes/2023/andres-leon.jpg`, `daniela-flores.jpg`… | Versiones de 160/320/640 px |
| Capturas PNG pesadas | `memorias/2020/*.png` (0,6–0,8 MB c/u) | WebP calidad 80 |
| Logos de patrocinadores en PNG | 5 logos | Solicitar SVG oficiales |
| Video MP4 local | `juego-cuidemonos/video-cuidemonos-play-utpl.mp4` (2,6 MB) | Mantener local con `preload="none"` y póster |

## 5. Videos de YouTube (todos verificados el 30-sep-2026)

| ID | Título en YouTube | Dónde |
|---|---|---|
| `W6CFvmTOYu0` | Virtual Reality Day Latam 2023 | Inicio (video destacado) |
| `Vhj5OXVEs1o` | VR DAY promocional Perú | Inicio (Voces) |
| `I7sxWPlXGug` | VR Day Latam - Colombia 2023 | Inicio (Voces) |
| `NlQJv8lMz-U` | Virtual Reality Day Latam 2023 - Ecuador - UTPL | Inicio (Voces) |
| `2t_razofWkY` | Virtual Reality Day 2022 | Memorias 2022 |
| `yJuiXWva9mo` | GAME JAM LATAM | Memorias 2022 |
| `GWPVuogsc40`, `3mH2c88h2_Q`, `BQ2y2sE4J5c` | (disponibles) | Memorias 2020 |
| `J9zWYuUNLNQ` | Día de la Realidad Virtual 2019 | Memorias 2019 |
| `M157uJOSa7U` | (disponible) | Realidad aumentada (heredada) |
| `O2Tj34g1tg0`, `dkoe2M7ousE` | Virtual Reality Day Latam 2021 · VRDay GameLatam | Memorias 2021 (antes 3 reproductores vacíos) |
