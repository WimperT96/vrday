# 03 · Arquitectura con Django

## 1. Objetivos que guían las decisiones

| Requisito | Decisión |
|---|---|
| Sitio 100 % informativo, sin base de datos ni formularios | Django **sin modelos**: el contenido se lee de archivos YAML. Se exporta a HTML estático. |
| Fácil cambiar la información | Todo el texto en `contenido/*.yaml`; todas las imágenes en `medios/`. Las plantillas no contienen texto del sitio. |
| Conservar páginas y estructura | Cada página del sitio actual = un YAML con sus secciones en el mismo orden. |
| Futuro: efectos, animaciones y 3D | Cada sección es un componente aislado con un "gancho" (`efectos:`) y JS cargado bajo demanda (ver `07-efectos-y-3d.md`). |

## 2. Pila tecnológica

| Capa | Elección | Nota |
|---|---|---|
| Framework | **Django 5.2 LTS** (soporte hasta abril 2028) | Solo plantillas, URLs y comandos. Sin `admin`, `auth` ni `sessions`. La última versión es 6.1; se prefiere la LTS por estabilidad (migrar a 6.2 LTS cuando salga en 2027). |
| Exportación | django-distill 4.x (activo, última versión sep-2026) | |
| Contenido | YAML (`PyYAML`) + Markdown en los campos de texto (`markdown`) | Validado con un comando propio. |
| Exportación estática | **django-distill** | Genera `dist/` con un HTML por URL. Se puede publicar en cualquier hosting estático. |
| Estilos | CSS nativo con variables (tokens de `02-identidad-visual.md §2`), sin framework | Opcional más adelante: Sass o Tailwind si el equipo lo prefiere. |
| JavaScript | Un solo módulo `static/js/main.js` sin dependencias (menú, diálogos, visor de galerías, pestañas, YouTube ligero, slider) + efectos cargados bajo demanda desde `static/js/efectos/` | Sin jQuery ni librerías externas: se descartaron Swiper/GLightbox porque lo necesario se resolvió con ~250 líneas propias. |
| Imágenes | Hoy: originales con `width`/`height`, `loading="lazy"`. Pendiente: versiones WebP/AVIF + `srcset` (fase 4) | Varios originales pesan varios MB (el fondo mide 6092 px). |
| Futuro 3D / efectos | Three.js, `<model-viewer>`, GSAP + ScrollTrigger | Ver `07-efectos-y-3d.md`. |

## 3. Estructura del proyecto Django (construida)

```
vrday/
├── manage.py
├── requirements.txt / requirements-dev.txt
├── vrday/                      proyecto Django
│   ├── settings.py             DATABASES = {} · apps: staticfiles, django_distill, sitio · medios/ → /static/medios/
│   ├── urls.py                 Inicio + <path:ruta>/ (todas las páginas y redirecciones salen de los YAML), sitemap, robots, 404
│   └── wsgi.py
├── sitio/                      app única
│   ├── contenido.py            cargador: lee y cachea los YAML (se recarga al guardar), resuelve `fuente:`, ponentes, galerías
│   ├── views.py                vista genérica `pagina` + redirecciones, sitemap.xml, robots.txt, 404
│   ├── context_processors.py   sitio, evento, menú (con ítem activo), botón Inscríbete, pie
│   ├── templatetags/vr.py      {% medio %} {% img %} {% enlace %} {% icono %} |md |md_linea |a_json |fecha_larga …
│   ├── tests.py                renderiza todas las páginas, redirecciones, enlaces e imágenes
│   └── management/commands/
│       ├── validar_contenido.py   medios, enlaces internos, plantillas faltantes, PENDIENTES
│       └── exportar.py            validar + collectstatic + distill → dist/
├── templates/
│   ├── base.html               <head> (SEO, Open Graph, canonical, fuentes), cabecera, pie, main.js
│   ├── pagina.html             recorre las secciones e incluye components/<tipo>.html
│   ├── partials/               header.html  footer.html  iconos.html (sprite SVG propio)
│   ├── components/             33 plantillas: una por tipo de sección + _youtube.html, _sesion.html
│   ├── redireccion.html  404.html  sitemap.xml  robots.txt
├── static/
│   ├── css/  tokens.css (identidad 2026) · base.css (layout, botones, cabecera, pie) · componentes.css (un bloque por tipo)
│   ├── js/   main.js · efectos/entrada.js (ejemplo del patrón de efectos)
│   └── img/decor/  circuito.svg · hexagonos.svg
├── contenido/  medios/  docs/  referencias/
└── dist/                       salida de `python manage.py exportar` (no se versiona)
```

### Flujo de una página

```
URL /agenda/  →  vrday/urls.py: <path:ruta>/  →  views.pagina(ruta="agenda")
             →  contenido.pagina("/agenda/")  (+ sitio.yaml, evento.yaml, ponentes.yaml)
             →  templates/pagina.html
                   for s in pagina.secciones:
                       <section class="seccion seccion--{tipo}" data-componente data-efectos>
                         include "components/{tipo}.html"
```

Agregar una página = crear su YAML en `contenido/paginas/` (la URL sale del campo `url:`). No hay que tocar código.

## 4. Formato del contenido

### Página (`contenido/paginas/*.yaml`)

```yaml
slug: acerca-de            # identificador único
url: /acerca-de/           # URL pública
titulo: Acerca de          # título (se usa en <title> y migas)
estado: publicada          # publicada | oculta (no sale en menú ni sitemap)
url_original: https://vrdaylatam.org/acerca-de/   # trazabilidad
seo: {titulo: ..., descripcion: ..., imagen: ...}  # opcional
secciones:                 # lista ordenada; cada una tiene "tipo"
  - tipo: texto
    id: que-es             # ancla (#que-es); opcional
    efectos: {}            # reservado para animaciones/3D; opcional
    ...campos del tipo...
```

Convenciones:
- Rutas de medios: relativas a `medios/` (`ponentes/2023/aura-forero.png`).
- Textos largos: bloque `|` con **Markdown** (negritas, listas, enlaces).
- Enlaces internos: empiezan con `/`. Externos: `https://…` (se abren en otra pestaña automáticamente).
- `placeholder: true` marca contenido de relleno heredado (se puede mostrar con un estilo distinto en modo borrador).
- `PENDIENTE` en un comentario = dato que falta; lo lista el validador.

### Ponentes (`contenido/ponentes.yaml`)

```yaml
- slug: aura-forero
  nombre: Aura Forero
  edicion: 2023
  pais: Colombia
  institucion: ''
  foto: ponentes/2023/aura-forero.png
  resena: |
    ...
  visible_en_sitio_actual: true   # tenía tarjeta visible en el sitio actual
  orden: 1                        # orden de aparición en la grilla
  notas: ...                      # observaciones de la migración (no se publican)
```

La sección `tipo: ponentes` filtra por `edicion` (y `solo_visibles`). Así, el mismo ponente se muestra en Inicio y Agenda sin duplicar la reseña.

## 5. Catálogo de secciones (componentes)

Cada tipo = `templates/components/<tipo>.html` + (si necesita) `static/css/components/<tipo>.css` y `static/js/components/<tipo>.js`.

| Tipo | Campos principales | Usado en | JS |
|---|---|---|---|
| `cabecera` | titulo, subtitulo, fondo, imagen | casi todas | — (futuro: fondo 3D) |
| `slider` | diapositivas[imagen, capa, alt, titulo, texto, botones[]] | Inicio | Swiper |
| `video_destacado` | titulo, subtitulo, youtube | Inicio | lite-youtube |
| `texto` | titulo, cuerpo (md), imagen, alt, ilustracion (rx/rv/ra/rm: SVG en `components/ilustraciones/`), imagen_posicion (izquierda/derecha/arriba/abajo), boton, fondo | casi todas | — |
| `estadisticas` | titulo, items[valor, etiqueta, icono] | Inicio | contador animado (futuro) |
| `inscripcion_paises` | mapa, boton_internacional, boton_pais, paises[nombre, bandera, url] | Inicio | — |
| `ponentes` | titulo, edicion, solo_visibles, fondo, mostrar | Inicio, Agenda, Memorias | modal de reseña |
| `tarjetas` | titulo, subtitulo, items[titulo, etiqueta, texto, imagen, url] | Inicio, Memorias, heredadas | — |
| `videos` | titulo, boton, items[titulo, youtube] | Inicio, Memorias | lite-youtube |
| `cta` | titulo, boton | Inicio | — |
| `botones` | items[texto, url, externo] | varias | — |
| `galeria` | titulo, imagenes[ruta o {src, alt}] **o** carpeta | Memorias, Plataforma, Stands, Juegos, Arte | GLightbox |
| `tabla` | titulo, columnas[], filas[[]] | Memorias 2019/2020 | — |
| `faq` | titulo, grupos[titulo, preguntas[pregunta, respuesta(md)]] | Centro de ayuda | `<details>` nativo |
| `acordeon` | items[titulo, cuerpo(md) o youtube], fondo | heredadas | `<details>` nativo |
| `formulario_externo` | titulo, url (Google Form), modo (incrustado/boton), texto_boton | Contacto | — |
| `embed` | titulo, proveedor (sketchfab/itch/google-maps/iframe), url, proporcion, alto, credito, boton{texto, url, icono} | Arte, Knockout | carga diferida |
| `video_local` | archivo | Juego Cuidémonos | — |
| `premios` | titulo, texto, items[titulo, subtitulo, imagen] | Juego Cuidémonos | — |
| `agenda_paises` | titulo, presentacion (pestanas/acordeon/lista), paises[id, nombre, bandera, ubicacion, inscripcion, sesiones[]] | Agenda | pestañas |
| `agenda_lista` | titulo, sesiones[hora, lugar, icono, titulo, ponentes, extra, moderador] | Agenda 2020 | — |
| `equipo` | titulo, miembros[nombre, cargo, foto] | heredadas | — |
| `testimonios` | titulo, items[nombre, cargo, foto] | heredadas | — |

### Tipos añadidos para la edición 2026

Estos tipos leen sus datos de `contenido/evento.yaml` (campo `fuente:`), para que el cambio de edición sea editar un solo archivo.

| Tipo | Campos principales | Usado en | JS |
|---|---|---|---|
| `hero_evento` | fuente: evento, logo, imagen, alt, video (id de YouTube, vertical 9:16), video_titulo, video_portada, boton_secundario | Inicio | video al hacer clic; efectos HUD (futuro) |
| `caracteristicas` | fuente: evento.caracteristicas (titulo, texto, icono) | Inicio | — |
| `inscripcion` | fuente: evento (inscripcion.texto/url + organizadores), titulo, texto, imagen, alt, texto_sin_enlace — sin URL el botón sale desactivado | Inicio | — |
| `convocatorias` | fuente: evento.convocatorias (titulo, fecha_limite, texto, url, boton) — se oculta sola al vencer | Inicio | — |
| `banda` | estilo (navy/claro), titulo (con `**palabra**` resaltada), subtitulo, imagen o nodos[{texto, icono}] (red de hasta 4 palabras unidas al isotipo; con nodos el titular va centrado y la red a todo el ancho) | Inicio | efecto `red_nodos` |
| `agenda_resumen` | fuente: agenda, destacar[], boton | Inicio | — |
| `agenda_dias` | tentativa, sedes[id, nombre, pais, bandera, dias[id, fecha, etiqueta, sesiones[hora, actividad, etiquetas[{texto, tono: info/alerta}], detalle, tipo, destacada], nota], nota] | Agenda 2026 | pestañas por día |
| `aliados` | fuente: evento (organizadores + aliados), titulo_sede, titulo_aliados — si falta el logo muestra el nombre | Inicio, pie | — |
| `logos` | titulo, items[nombre, logo, url] | Memorias 2023 | — |

Campos nuevos en tipos existentes: `ponentes.mensaje_vacio` (texto si no hay ponentes de esa edición), `embed.imagen_respaldo` (imagen mientras no haya URL), `botones.titulo`.

**Agregar un tipo nuevo** = crear su plantilla (y CSS/JS si aplica) y usarlo en un YAML. No hay que tocar vistas ni URLs.

## 6. Comandos

| Comando | Qué hace |
|---|---|
| `python manage.py runserver` | Servidor de desarrollo en http://127.0.0.1:8000 (el contenido se recarga al guardar un YAML; muestra las marcas "Contenido provisional") |
| `python manage.py validar_contenido` | Revisa YAML, imágenes, enlaces internos, plantillas y lista los PENDIENTES |
| `python manage.py test sitio` | Renderiza todas las páginas y verifica enlaces, imágenes y redirecciones |
| `python manage.py exportar` | Valida y genera el sitio estático completo en `dist/` (sin marcas de borrador) |
| `python manage.py exportar --borrador` | Igual, pero mostrando las marcas de contenido provisional (para revisión interna) |
| `python -m http.server 8080 --directory dist` | Previsualizar el sitio exportado |

`dist/` es un sitio estático completo: se sube a cualquier hosting (servidor de la universidad, GitHub Pages, Netlify, Cloudflare Pages).

- **Redirecciones**: cada URL antigua de `sitio.yaml → redirecciones` se exporta como una página HTML con `meta refresh` + `location.replace` + `canonical`. Si el hosting admite reglas 301 (Nginx, `_redirects`), conviene declararlas también (pendiente E3).
- **URLs con barra final** (`/acerca-de/` → `acerca-de/index.html`), igual que hoy.
- **Fecha de corte**: las convocatorias vencidas se ocultan **al exportar**; hay que volver a exportar después de la fecha límite.
- El aviso "MEDIA_URL and MEDIA_ROOT must be set" de distill es inofensivo: el sitio no usa archivos subidos por usuarios.

## 7. SEO, rendimiento y accesibilidad

- `<title>`, meta descripción, Open Graph y Twitter Card por página (desde `seo:` o valores por defecto de `sitio.yaml`).
- `sitemap.xml` y `robots.txt` generados (solo páginas `publicada`).
- `<link rel="canonical">` en todas las páginas.
- Imágenes con `width`/`height`, `loading="lazy"` (excepto la primera del slider) y `srcset`.
- YouTube con fachada ligera (miniatura + clic) y dominio `youtube-nocookie.com`.
- Menú accesible por teclado, modales con foco atrapado y cierre con Esc, `prefers-reduced-motion` respetado por todo efecto.
- Analítica (GTM/GA4 actuales en `sitio.yaml`) opcional; si se mantiene, cargarla después de la interacción o con aviso de cookies.
