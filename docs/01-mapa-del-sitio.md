# 01 · Mapa del sitio

## 0. Nuevo menú 2026 (aplicado)

```
Inicio · Acerca de · Ponentes · Agenda · Lugar · Memorias ▾ · Contacto        [Inscríbete →]
                                                   ├─ VRD 2023   /memorias/2023/
                                                   ├─ VRD 2022   /memorias/2022/
                                                   ├─ VRD 2021 · VRD 2020 · VRD 2019
Pie: Plataforma inmersiva · Centro de ayuda · Memorias · Contacto + sede organizadora y aliados 2026
```

- **Inicio** y **Agenda** ahora muestran la edición **2026** (maqueta + agenda tentativa).
- El contenido 2023 que estaba en Inicio y Agenda se movió a `/memorias/2023/` y `/memorias/2023/agenda/` sin cambios.
- **Ponentes** y **Lugar** son páginas nuevas (de la maqueta).
- **Plataforma inmersiva** y **Centro de ayuda** siguen existiendo en la misma URL, enlazadas desde el pie.
- Los auspiciantes 2023 del pie pasaron a `/memorias/2023/`; el pie muestra la sede y los aliados 2026.
- El botón **Inscríbete** aparecerá cuando exista el enlace de inscripción (`09-pendientes.md` A2).

Las secciones 2 a 6 describen el **sitio actual** (antes del cambio) y la migración.

## 1. Cómo se obtuvo

- Sitemap oficial (`/wp-sitemap.xml`) + API de WordPress (`/wp-json/wp/v2/pages`) + menú del encabezado.
- Se descargó el HTML de cada página (`referencias/captura-sitio-actual/html/`) y se convirtió a texto por secciones (`…/texto/`).
- Tecnología actual: WordPress 7 · tema **Kallyas 4.18** con constructor Zion · Revolution Slider · TablePress · W3 Total Cache.
- Las imágenes se referencian desde un dominio antiguo (`virtualrealityday.utpl.edu.ec`) que **ya responde 404**; los mismos archivos existen en `vrdaylatam.org/wp-content/uploads/…` y de ahí se descargaron.

## 2. Menú principal actual

```
INICIO
ACERCA DE
AGENDA
PLATAFORMA INMERSIVA
MEMORIAS ▾            (enlace "#", solo despliega)
   ├─ VRD 2022        → /vrd-2023/   ⚠ el slug dice 2023
   ├─ VRD 2021        → /vrd-2021/
   ├─ VRD 2020        → /vrd-2020/
   └─ VRD 2019        → /vrd-2019/
CENTRO DE AYUDA
CONTACTO
```

No hay menú en el pie. El pie solo muestra "AUSPICIAN:" y 5 logos (COP, Globant, iLRN, Unity, Libel Academy).

## 3. Inventario de páginas

**Estado nuevo:** `publicada` = en menú o enlazada · `oculta` = accesible por URL pero fuera del menú (igual que hoy) · `descartada` = no se migra.

| # | Página | URL actual | URL nueva | Cómo se llega hoy | Estado nuevo | Archivo de contenido |
|---|---|---|---|---|---|---|
| 1 | Inicio **2026** (nuevo contenido) | `/` | `/` | Menú | publicada | `paginas/inicio.yaml` |
| 1b | Inicio 2023 (contenido anterior) | `/` | `/memorias/2023/` | Menú › Memorias | publicada | `paginas/memorias/2023.yaml` |
| 2 | Acerca de | `/acerca-de/` | `/acerca-de/` | Menú | publicada | `paginas/acerca-de.yaml` |
| 3 | Agenda **2026** (tentativa, sede UTPL) | `/agenda/` | `/agenda/` | Menú | publicada | `paginas/agenda.yaml` |
| 3b | Agenda 2023 (6 países) | `/agenda/` | `/memorias/2023/agenda/` | Memorias 2023 | publicada | `paginas/memorias/2023-agenda.yaml` |
| 3c | **Ponentes** | — (nueva) | `/ponentes/` | Menú | publicada | `paginas/ponentes.yaml` |
| 3d | **Lugar** | — (nueva) | `/lugar/` | Menú | publicada | `paginas/lugar.yaml` |
| 4 | Plataforma inmersiva | `/plataforma-inmersiva/` | `/plataforma-inmersiva/` | **Pie** (antes menú) | publicada | `paginas/plataforma-inmersiva.yaml` |
| 5 | **Memorias (índice)** | — (no existía) | `/memorias/` | **Nuevo** | publicada | `paginas/memorias/index.yaml` |
| 6 | VRD 2022 | `/vrd-2023/` | `/memorias/2022/` | Menú › Memorias | publicada | `paginas/memorias/2022.yaml` |
| 7 | VRD 2021 | `/vrd-2021/` | `/memorias/2021/` | Menú › Memorias | publicada | `paginas/memorias/2021.yaml` |
| 8 | VRD 2020 | `/vrd-2020/` | `/memorias/2020/` | Menú › Memorias | publicada | `paginas/memorias/2020.yaml` |
| 9 | VRD 2019 | `/vrd-2019/` | `/memorias/2019/` | Menú › Memorias | publicada | `paginas/memorias/2019.yaml` |
| 10 | Centro de ayuda | `/centro-de-ayuda/` | `/centro-de-ayuda/` | **Pie** (antes menú) | publicada | `paginas/centro-de-ayuda.yaml` |
| 11 | Contacto | `/contacto/` | `/contacto/` | Menú | publicada | `paginas/contacto.yaml` |
| 12 | Arte en cuarentena | `/arte-en-cuarentena/` | igual | Tarjeta en Inicio, FAQ | publicada | `paginas/arte-en-cuarentena.yaml` |
| 13 | Red de Aprendizaje Inmersivo (iLRN) – Ecuador | `/red-de-aprendizaje-inmersivo-ilrn-ecuador/` | igual | Tarjeta en Inicio | publicada | `paginas/red-de-aprendizaje-inmersivo-ilrn-ecuador.yaml` |
| 14 | Juego VR Knock Out | `/juego-knockout/` | igual | Slider del Inicio | publicada | `paginas/juego-knockout.yaml` |
| 15 | Juego Cuidémonos Play-UTPL | `/juego-cuidemonos-play-utpl/` | igual | FAQ del Centro de ayuda | publicada | `paginas/juego-cuidemonos-play-utpl.yaml` |
| 16 | Stands virtuales | `/stands-virtuales/` | igual | Ninguno (huérfana) | oculta | `paginas/stands-virtuales.yaml` |
| 17 | Agenda 2020 | `/agenda-2019/` | `/memorias/2020/agenda/` | Ninguno (huérfana) | oculta* | `paginas/memorias/2020-agenda.yaml` |
| 18 | Acerca de VRD anterior (2020) | `/acerca-de-vrd-anterior/` | `/memorias/2020/acerca-de/` | Ninguno (huérfana) | oculta* | `paginas/memorias/2020-acerca-de.yaml` |
| 19 | Realidad aumentada (grupo DTE) | `/realidad-aumentada/` | igual | Ninguno (huérfana) | oculta | `paginas/heredadas/realidad-aumentada.yaml` |
| 20 | Inicio – ARIES (grupo DTE) | `/inicio-aries/` | igual | Ninguno (huérfana) | oculta | `paginas/heredadas/inicio-aries.yaml` |
| 21 | Acordeón | `/acordeon/` | igual | Ninguno (huérfana) | oculta | `paginas/heredadas/acordeon.yaml` |
| — | Prueba | `/prueba/` | → `/` | Ninguno | **descartada** | — (página vacía de WordPress) |
| — | Portfolio (12 fichas) | `/portfolio/*`, `/project_category/*` | → `/` | Ninguno | **descartada** | — (contenido demo del tema, en inglés, lorem ipsum) |
| — | Plantillas internas | `/layout_manager/…`, `/znpb_template_mngr/…` | — | Ninguno | **descartada** | — (plantillas del constructor; su contenido = encabezado y pie, ya migrados) |

\* Desde `/memorias/2020/` se añaden dos botones hacia estas páginas (antes eran inalcanzables). Si prefieres mantenerlas totalmente ocultas, basta con borrar la sección `botones` de `memorias/2020.yaml`.

## 4. Mejoras de estructura aplicadas (sin cambiar contenido)

| Mejora | Motivo | Cómo revertir |
|---|---|---|
| URLs de memorias pasan a `/memorias/<año>/` | `/vrd-2023/` mostraba la edición 2022; ahora URL = año real. Se crean redirecciones 301 desde las URLs antiguas. | Cambiar `url:` en los YAML de `memorias/`. |
| Nueva página índice `/memorias/` | El menú "Memorias" no llevaba a ninguna parte. La página solo enlaza a las 4 ediciones. | Quitar la página y poner `url: ""` en el menú. |
| `/agenda-2019/` → `/memorias/2020/agenda/` | Su contenido es de 2020 (VirBELA, juego Covid-19, Arte en cuarentena). | — |
| Anclas legibles en la Agenda (`#colombia`, `#peru`…) | Antes eran IDs internos (`#eluid22a08e12`). Las banderas del Inicio apuntan a ellas. | — |
| Los ponentes se definen **una sola vez** (`ponentes.yaml`) | Hoy la misma reseña está copiada en Inicio y en Agenda, con diferencias entre copias. | — |
| Ponentes 2021 recuperados | 19 reseñas de 2021 existen como modales ocultos de la Agenda. Quedan listas para mostrarse en `/memorias/2021/` (desactivado: `mostrar: false`). | — |

## 5. Redirecciones (URL antigua → nueva)

Definidas en `contenido/sitio.yaml → redirecciones`:

```
/vrd-2023/               → /memorias/2022/
/vrd-2021/               → /memorias/2021/
/vrd-2020/               → /memorias/2020/
/vrd-2019/               → /memorias/2019/
/agenda-2019/            → /memorias/2020/agenda/
/acerca-de-vrd-anterior/ → /memorias/2020/acerca-de/
/prueba/                 → /
/portfolio/*             → /
```

En un sitio estático, cada redirección se genera como una pequeña página HTML con `<meta http-equiv="refresh">` + `<link rel="canonical">`. Si el hosting lo permite (Nginx, Netlify, Cloudflare Pages), conviene además declararlas como 301 reales (ver `docs/03`).

## 6. Estructura de cada página (resumen)

| Página | Secciones, en orden |
|---|---|
| **Inicio** | Slider (4 artes) → Video "La Realidad eXtendida (RX)" → ¿Qué es el VRD? → Cifras (800 participantes · 70+ expositores · 8 países) → Inscripciones (internacional / por país + mapa + 8 banderas) → Ponentes latinoamericanos (40, con modal de reseña) → Tarjetas de actividades (5) → Voces VRDay Latam (3 videos) → CTA "Entérate lo que fue el VRD 2022" |
| **Acerca de** | Cabecera ilustrada → ¿Qué es el Día de la RV? → ¿Quién organiza? → ¿Qué es RX? (con ilustración) → ¿Qué es RV? → ¿Qué es RA? → ¿Qué es RM? |
| **Agenda** | Cabecera → Jornada por países (Colombia, Ecuador, Perú, Brasil, Bolivia, Chile: ubicación, enlace de inscripción, programa) → Ponentes (40, con modal) |
| **Plataforma inmersiva** | Cabecera → Pasos para ingresar (infografía) → Información adicional → Botón "Descargar manuales" → Galería VirBELA (7) |
| **Memorias 2019–2022** | Título → Galería de fotos → Tabla (2019: actividades · 2020: agenda) → Videos |
| **Centro de ayuda** | Cabecera → Botón "Ayuda en línea" (Discord) → FAQ en 4 grupos (VRD, Arte en cuarentena, Juego Cuidémonos, iLRN) |
| **Contacto** | Cabecera → Formulario (Nombre, E-mail, Asunto, Mensaje) → se reemplaza por Google Form |
| **Arte en cuarentena** | Cabecera → Descripción → Curadora María Elisa Flores → Modelo 3D Sketchfab → Instrucciones (2 imágenes) |
| **iLRN Ecuador** | Cabecera → Imagen + descripción y objetivos |
| **Juego Knockout** | Cabecera con logo → Juego embebido (itch.io) → ¿Cómo jugar? → Premios |
| **Juego Cuidémonos** | Cabecera → Video MP4 → Descripción → Pasos → Reto → Premios (2) → Galería (16) |
| **Stands virtuales** | Cabecera → Descripción + lista de expositores → Galería (5) |
