# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Rebuild of https://vrdaylatam.org/ (formerly WordPress) as a **static site generated with Django**. There are no models, no database (`DATABASES = {}`), no admin, auth or sessions. All site text lives in YAML under `contenido/`, all images in `medios/`, and `django-distill` exports everything to HTML in `dist/`. The code, comments, docs, YAML keys and commit messages are all in **Spanish**. Keep that convention.

`docs/` holds the design decisions. Read `docs/03-arquitectura-django.md` for the full content format and section catalog, `docs/09-pendientes.md` for open items, and `docs/07-efectos-y-3d.md` for the animation/3D hooks.

## Commands

Python 3.12, with the venv at `.venv/` (`.venv\Scripts\activate` on Windows).

```powershell
pip install -r requirements.txt          # site only (CI uses this)
pip install -r requirements-dev.txt      # + scraping/migration tools in referencias/herramientas/
python manage.py runserver               # dev server; YAML edits reload automatically, placeholders are marked
python manage.py test sitio              # the whole test suite (renders every page)
python manage.py test sitio.tests.PaginasTest.test_redirecciones   # a single test
python manage.py validar_contenido       # missing media, broken internal links, missing component templates, PENDIENTE list
python manage.py exportar                # validate + collectstatic + distill → dist/ (placeholder marks hidden)
python manage.py exportar --borrador     # same, but placeholder marks stay visible
python -m http.server 8080 --directory dist
```

There is no linter configured.

To reproduce the GitHub Pages build locally (subfolder deploy plus noindex):
```powershell
$env:VR_BASE_URL="/vrday"; $env:VR_NOINDEX="1"; .venv\Scripts\python.exe manage.py exportar --borrador
Remove-Item Env:VR_BASE_URL, Env:VR_NOINDEX
```
In Git Bash, prefix the command with `MSYS_NO_PATHCONV=1`. Otherwise Git Bash rewrites `/vrday` into a Windows path.

CI (`.github/workflows/publicar-pages.yml`) runs on every push to `main`: tests, then `exportar --borrador` with `VR_BASE_URL=/<repo>` and `VR_NOINDEX=1`, then deploy to GitHub Pages.

## Architecture

**Request flow:** `vrday/urls.py` has one catch-all `<path:ruta>/` route plus `""`, and both go to `sitio/views.py:pagina`. Sitemap, robots and `404.html` have their own small views. `pagina` first checks `sitio.yaml → redirecciones`, then looks the URL up in `contenido.cargar().paginas`, which is keyed by each YAML's `url:` field after normalizing it to `/x/`. It then renders `templates/pagina.html`, which loops over `pagina.secciones` and includes `templates/components/<tipo>.html` for each section. Every section is wrapped in `<section class="seccion seccion--<tipo>" data-componente data-efectos>` with a `.seccion__fondo` layer.

- **Redirects** (old WordPress URLs) can't be real 301s on a static host. Each one is exported as its own page from `templates/redireccion.html` (meta refresh + canonical). The 404 works the same way: `handler404` covers the dev server, and an exportable `/404.html` covers the host.
- Templates in `components/` that start with `_` (`_sesion.html`, `_youtube.html`) are partials shared by several section types, not section types themselves.

- **Adding a page** = add a YAML file under `contenido/paginas/`. URLs and export routes are derived automatically: `_rutas_paginas()` in `urls.py` feeds distill. A YAML with no `url:` key is silently ignored.
- **Adding a section type** = add `templates/components/<tipo>.html` (plus CSS in `static/css/componentes.css` if needed). `validar_contenido` fails if a YAML uses a `tipo` with no template.
- **Adding an effect** = add `static/js/efectos/<nombre>.js` exporting `default(elemento, config)` and register it in the `efectos` map in `static/js/main.js`. YAML `efectos: {nombre: config}` becomes `data-efectos` JSON, and effects are skipped under `prefers-reduced-motion`.

**`sitio/contenido.py`** is the core of the site:
- `cargar()` reads `sitio.yaml`, `evento.yaml`, `ponentes.yaml` and every `paginas/**/*.yaml`. It caches them in memory and reloads only when some YAML's mtime changes.
- `resolver_seccion()` keeps logic out of templates. It fills in derived data per `tipo`:
  - `ponentes` filters `ponentes.yaml` by `edicion`.
  - `galeria` can list a whole `medios/` folder via `carpeta`.
  - `hero_evento`/`aliados` inject `evento` and the formatted dates.
  - `caracteristicas`/`convocatorias` pull from `evento.yaml` through `fuente:`.
  - `agenda_resumen` reads the `agenda_dias` section of `/agenda/`.
- Expired `convocatorias` (`fecha_limite` < today) are dropped **at export time**, so the site must be re-exported after deadlines pass.
- Sections with `mostrar: false` are skipped. Organizers or allies with `publicar: false` stay in the YAML but are hidden.
- `evento.yaml` is the single file to edit when changing editions.

**Subfolder deployment (`VR_BASE_URL` → `settings.SITIO_BASE`):** every internal URL must go through `contenido.url_sitio()` or the template helpers `{% ruta %}` / `{% enlace %}`. Never hardcode `/...` hrefs in templates. `exportar` moves distill's nested `dist/<base>/static` back up to `dist/static`. `test_publicacion_en_subcarpeta` covers this.

**Template helpers** (`sitio/templatetags/vr.py`, registered as builtins, so no `{% load %}` is needed): `{% medio %}`, `{% img %}` (adds width/height from the real file, plus lazy loading), `{% enlace %}` (externals get `target="_blank"`), `{% ruta %}`, `{% icono %}` (sprite in `templates/partials/iconos.html`), plus the `|md`, `|md_linea`, `|a_json` and `|fecha_larga` filters.

**Static files:** `medios/` is served under `/static/medios/` (a `STATICFILES_DIRS` prefix), so content refers to media by paths relative to `medios/`, e.g. `ponentes/2023/aura-forero.png`. The CSS is plain CSS: `tokens.css` holds the 2026 brand tokens from `docs/02-identidad-visual.md`, `base.css` the layout, and `componentes.css` one block per section type. JS is a single dependency-free ES module, `main.js`, and each feature in it only activates if its component is present.

**Settings flags (all from env vars):** `DJANGO_DEBUG` defaults to `1`. `MOSTRAR_PLACEHOLDERS` (`VR_MOSTRAR_PLACEHOLDERS`) controls whether `placeholder: true` sections get a "Contenido provisional" mark. It defaults to on with `DEBUG` and is overridden by `exportar`. `NO_INDEXAR` comes from `VR_NOINDEX`, and `SITIO_BASE` from `VR_BASE_URL`.

**Tests** use `SimpleTestCase` (there is no DB) and render every page through the test client. Because they read the real `contenido/`, a content change can break them too.

## Content conventions

- Long text fields are Markdown in `|` blocks. Internal links start with `/` and are validated. External links start with `https://`.
- `PENDIENTE` in a YAML comment marks missing data, and the validator lists these. `placeholder: true` marks filler content.
- `estado: oculta` pages (e.g. `paginas/heredadas/`) are still rendered and exported but stay out of the menu and sitemap.
- The validator logic lives in `referencias/herramientas/validar_contenido.py`, which the `validar_contenido` management command runs via `runpy`.
- `referencias/` is backup material (the scraped original site, migration scripts) and is not published. `dist/` and `staticfiles/` are generated and gitignored.
