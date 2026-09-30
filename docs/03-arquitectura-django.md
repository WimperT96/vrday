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
| JavaScript | Módulos ES nativos, uno por componente, cargados solo si la sección existe en la página | Sin jQuery. |
| Librerías puntuales | Swiper (slider), GLightbox (galerías), lite-youtube-embed (videos) | Todas vía npm o archivo local en `static/vendor/`. |
| Imágenes | Pillow → versiones WebP/AVIF en varios anchos + `<picture>` con `srcset` | Varios originales pesan varios MB (el fondo mide 6092 px). |
| Futuro 3D / efectos | Three.js, `<model-viewer>`, GSAP + ScrollTrigger | Ver `07-efectos-y-3d.md`. |

## 3. Estructura del proyecto Django (propuesta)

```
vrday/
├── contenido/                  ← (ya existe) YAML: fuente de verdad
├── medios/                     ← (ya existe) imágenes y videos
├── manage.py
├── requirements.txt            Django, django-distill, PyYAML, Markdown, Pillow
├── vrday/                      proyecto Django
│   ├── settings.py             DATABASES = {} · INSTALLED_APPS mínimas · STATICFILES_DIRS
│   └── urls.py
├── sitio/                      app única
│   ├── contenido.py            cargador: lee y cachea YAML, resuelve ponentes, valida
│   ├── views.py                una sola vista genérica: pagina(url) -> plantilla pagina.html
│   ├── urls.py                 rutas generadas desde los YAML + redirecciones (distill)
│   ├── templatetags/
│   │   └── vr.py               {% imagen %}, {% youtube %}, |markdown, {% seccion %}
│   └── management/commands/
│       ├── validar_contenido.py   (= referencias/herramientas/validar_contenido.py)
│       └── optimizar_imagenes.py  genera WebP/AVIF responsive en static/medios-opt/
├── templates/
│   ├── base.html               <head>, SEO, fuentes, tokens, header, footer, carga de JS
│   ├── partials/  header.html  footer.html  menu.html  modal-ponente.html
│   ├── pagina.html             recorre pagina.secciones e incluye components/<tipo>.html
│   └── components/             UNA plantilla por tipo de sección (ver catálogo)
│       ├── cabecera.html  texto.html  galeria.html  videos.html  ponentes.html …
├── static/
│   ├── css/  tokens.css  base.css  components/<tipo>.css
│   ├── js/   main.js (registro de componentes)  components/<tipo>.js  efectos/*.js
│   ├── vendor/                 librerías de terceros
│   └── modelos-3d/             (futuro) .glb / .gltf
└── dist/                       salida de `python manage.py distill-local` (no se versiona)
```

### Flujo de una página

```
URL /agenda/  →  sitio.urls (generada desde contenido/paginas/agenda.yaml)
             →  views.pagina(slug="agenda")
             →  contenido.cargar_pagina("agenda")  (+ sitio.yaml, + ponentes.yaml)
             →  templates/pagina.html
                   for seccion in pagina.secciones:
                       include "components/{{ seccion.tipo }}.html"
```

`pagina.html` (idea):

```django
{% extends "base.html" %}
{% block contenido %}
  {% for s in pagina.secciones %}
    {% if s.mostrar is not False %}
    <section id="{{ s.id|default:'' }}" class="seccion seccion--{{ s.tipo }}"
             data-componente="{{ s.tipo }}"
             {% if s.efectos %}data-efectos='{{ s.efectos|json }}'{% endif %}>
      {% include "components/"|add:s.tipo|add:".html" with s=s %}
    </section>
    {% endif %}
  {% endfor %}
{% endblock %}
```

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
| `texto` | titulo, cuerpo (md), imagen, imagen_posicion (izquierda/derecha/arriba/abajo), boton, fondo | casi todas | — |
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
| `embed` | titulo, proveedor (sketchfab/itch/iframe), url, proporcion, alto, credito | Arte, Knockout | carga diferida |
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
| `hero_evento` | fuente: evento, logo, imagen, alt, boton_secundario | Inicio | efectos HUD (futuro) |
| `caracteristicas` | fuente: evento.caracteristicas (titulo, texto, icono) | Inicio | — |
| `convocatorias` | fuente: evento.convocatorias (titulo, fecha_limite, texto, url) — se oculta sola al vencer | Inicio | — |
| `banda` | estilo (navy/claro), titulo (con `**palabra**` resaltada), subtitulo, imagen | Inicio | — |
| `agenda_resumen` | fuente: agenda, destacar[], boton | Inicio | — |
| `agenda_dias` | tentativa, sedes[id, nombre, pais, bandera, dias[id, fecha, etiqueta, sesiones[hora, actividad, detalle, tipo, destacada]], nota] | Agenda 2026 | pestañas por día |
| `aliados` | fuente: evento (organizadores + aliados), titulo_sede, titulo_aliados — si falta el logo muestra el nombre | Inicio, pie | — |
| `logos` | titulo, items[nombre, logo, url] | Memorias 2023 | — |

Campos nuevos en tipos existentes: `ponentes.mensaje_vacio` (texto si no hay ponentes de esa edición), `embed.imagen_respaldo` (imagen mientras no haya URL), `botones.titulo`.

**Agregar un tipo nuevo** = crear su plantilla (y CSS/JS si aplica) y usarlo en un YAML. No hay que tocar vistas ni URLs.

## 6. Exportación y publicación

```bash
python manage.py validar_contenido          # 0 errores antes de publicar
python manage.py optimizar_imagenes         # genera versiones WebP/AVIF
python manage.py collectstatic --noinput
python manage.py distill-local dist/ --force
```

`dist/` es un sitio estático completo: se sube a cualquier hosting (servidor Nginx de la universidad, GitHub Pages, Netlify, Cloudflare Pages).

- **Redirecciones**: django-distill genera una página HTML por cada redirección de `sitio.yaml` (meta refresh + canonical). Si el hosting admite reglas (`_redirects` de Netlify/Cloudflare o `return 301` de Nginx), el comando de exportación puede generar también ese archivo.
- **URLs con barra final** (`/acerca-de/` → `acerca-de/index.html`), igual que hoy: los enlaces existentes siguen funcionando.
- **Durante el desarrollo** se usa `python manage.py runserver` normal; el contenido se recarga al guardar el YAML.

## 7. SEO, rendimiento y accesibilidad

- `<title>`, meta descripción, Open Graph y Twitter Card por página (desde `seo:` o valores por defecto de `sitio.yaml`).
- `sitemap.xml` y `robots.txt` generados (solo páginas `publicada`).
- `<link rel="canonical">` en todas las páginas.
- Imágenes con `width`/`height`, `loading="lazy"` (excepto la primera del slider) y `srcset`.
- YouTube con fachada ligera (miniatura + clic) y dominio `youtube-nocookie.com`.
- Menú accesible por teclado, modales con foco atrapado y cierre con Esc, `prefers-reduced-motion` respetado por todo efecto.
- Analítica (GTM/GA4 actuales en `sitio.yaml`) opcional; si se mantiene, cargarla después de la interacción o con aviso de cookies.
