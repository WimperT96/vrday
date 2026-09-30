# 08 · Plan de trabajo

## Fase 0 — Recopilación ✅ (hecha)

- [x] Inventario de todas las páginas, menú y pie (`01`)
- [x] Todo el texto en YAML estructurado (`contenido/`)
- [x] 71 ponentes unificados (`contenido/ponentes.yaml`)
- [x] 187 medios descargados, renombrados y ordenados (`medios/`); 11 placeholders
- [x] Identidad actual analizada y propuesta de tokens (`02`)
- [x] Arquitectura Django definida (`03`)
- [x] Problemas de contenido listados (`06`)
- [x] Script de validación (`referencias/herramientas/validar_contenido.py`)

## Fase 1 — Decisiones (tuyas) antes de construir

> Lista completa y actualizada de pendientes: **`09-pendientes.md`**.

- [x] Enviar las **imágenes de identidad visual** → recibidas y validadas (`02`)
- [ ] Pedir al diseñador los recursos en vector (`02 §6`) y aplicar los 3 ajustes obligatorios (contraste, azul único, logo SVG)
- [x] Menú 2026 aprobado y aplicado (`01 §0`)
- [x] Agenda tentativa 2026 cargada (`paginas/agenda.yaml`)
- [ ] Datos 2026 que faltan (sede, inscripción, postulación) → se completan con la web funcionando (`09 §A`)
- [ ] Confirmar las mejoras de URL de Memorias y las redirecciones (`01 §4–5`)
- [ ] ¿Se conservan las 3 páginas heredadas (`/realidad-aumentada/`, `/inicio-aries/`, `/acordeon/`) o se retiran? (hoy: ocultas)
- [x] Contenido 2023 movido a `/memorias/2023/`; Inicio rehecho para 2026
- [ ] Crear el **Google Form de contacto** (`05 §1`)
- [ ] ¿Se mantienen Google Tag Manager / Analytics?
- [ ] Hosting destino (servidor UTPL, GitHub Pages, Netlify, Cloudflare Pages…)

## Fase 2 — Esqueleto Django

- [x] Repositorio git + entorno virtual con dependencias fijadas

- [ ] Proyecto Django 5.2 + app `sitio` + `requirements.txt`
- [ ] Cargador de YAML y vista genérica (`03 §3`)
- [ ] `base.html` con header (menú + submenú), footer (auspiciantes) y SEO
- [ ] `tokens.css` + `base.css` (tokens 2026 de `02 §2`, Poppins, tema claro + secciones navy)
- [ ] Comando `validar_contenido` (portar el script existente)
- [ ] Exportación con django-distill + redirecciones
- **Resultado:** todas las URLs responden con cabecera y texto plano.

## Fase 3 — Componentes (en orden de impacto)

1. [ ] `cabecera`, `texto`, `botones`, `cta` → cubren la mayoría de páginas
2. [ ] `ponentes` + modal de reseña → Inicio y Agenda
2b. [ ] **Tipos 2026**: `hero_evento`, `caracteristicas`, `convocatorias`, `banda`, `agenda_dias`, `agenda_resumen`, `aliados` → Inicio y Agenda 2026 (prioridad si se publica primero solo el Inicio, ver `09 A4`)
3. [ ] `galeria` (lightbox) → Memorias, Plataforma, Stands, Juegos
4. [ ] `videos`, `video_destacado` (YouTube ligero) → Inicio y Memorias
5. [ ] `agenda_paises` (pestañas por país) → Agenda
6. [ ] `slider`, `estadisticas`, `inscripcion_paises`, `tarjetas` → Inicio
7. [ ] `faq`, `acordeon`, `tabla`, `formulario_externo`, `embed`, `video_local`, `premios`
8. [ ] `agenda_lista`, `equipo`, `testimonios` → páginas 2020 y heredadas

## Fase 4 — Calidad y publicación

- [ ] Optimización de imágenes (WebP/AVIF + `srcset`)
- [ ] Accesibilidad (teclado, foco, contraste, textos alternativos)
- [ ] Lighthouse móvil ≥ 90 en Rendimiento, Accesibilidad, SEO
- [ ] Revisión visual página por página contra el sitio actual (`referencias/captura-sitio-actual/`)
- [ ] Publicación + prueba de todas las redirecciones
- [ ] Apuntar el dominio `vrdaylatam.org`

## Fase 5 — Dinamismo (posterior)

- [ ] Efectos de entrada y contadores (bajo costo)
- [ ] Fondo 3D de partículas en cabeceras
- [ ] Modelos 3D (`<model-viewer>`) y experiencias WebXR
- Ver `07-efectos-y-3d.md`.

## Cómo actualizar contenido una vez publicado

1. Editar el YAML correspondiente (o agregar imágenes en `medios/`).
2. `python manage.py validar_contenido`
3. `python manage.py distill-local dist/ --force`
4. Subir `dist/` al hosting (o dejar que un flujo automático lo haga al hacer *push*).
