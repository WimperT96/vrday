# 09 · Pendientes

Lista única de todo lo que falta. Se revisa al terminar cada fase.
Los datos marcados `PENDIENTE` dentro de los YAML se listan automáticamente con:

```
python referencias/herramientas/validar_contenido.py
```

---

## A. Para después de tener la web funcionando (acordado dejarlos así por ahora)

| # | Pendiente | Dónde se completa | Nota |
|---|---|---|---|
| A1 | **Sede 2026 — detalles para la página "Lugar"**: dirección exacta, mapa (URL de Google Maps), fotos, indicaciones de llegada | `contenido/evento.yaml → lugar`, `contenido/paginas/lugar.yaml` | Ya se sabe: UTPL (Loja), Centro de Convenciones UTPL, stands en el Hall del Aula Magna y en el sector de ingreso al Rectorado (dato de la agenda) |
| A2 | **Enlace de inscripción 2026** | `contenido/evento.yaml → inscripcion.url` | Mientras esté vacío, el botón "Inscríbete" del menú no se muestra y el del hero queda sin enlace |
| A3 | **Enlace de postulación de artículos** | `contenido/evento.yaml → convocatorias[0].url` | |
| A4 | **Plazo de postulación: 15 de octubre de 2026** (15 días desde el 30-sep). Si la web debe difundir la convocatoria, el calendario es muy justo. Opción: publicar primero solo el Inicio 2026 (hero + convocatoria + agenda) y migrar el resto después | Decisión de calendario | La convocatoria se oculta sola cuando pasa la fecha límite |

## B. Recursos gráficos (pedir al diseñador)

| # | Recurso | Estado actual |
|---|---|---|
| B1 | Logo 2026 en SVG: horizontal, apilado, isotipo, versión blanca | Provisional: `medios/marca/logo-vrday-2026-provisional.png` (recorte de la maqueta, 360×64) · placeholders `logo-vrday-2026-apilado.svg`, `isotipo-visor.svg` |
| B2 | Nombre/licencia de la fuente de "DAY" y "12 Y 13 DE" | — |
| B3 | Foto del hero (persona con visor) en alta resolución + derechos de uso | Placeholder `medios/inicio-2026/hero-persona-vr.svg` |
| B4 | Foto de la banda navy | Placeholder `medios/inicio-2026/banda-conecta.svg` |
| B5 | Logos individuales de UTPL, RAIN y 16 aliados | Solo existen dentro del afiche; mientras tanto se muestran los nombres |
| B6 | Patrones SVG (circuitos, hexágonos, anillos HUD) | — |
| B7 | Favicon, `apple-touch-icon`, imagen para redes 1200×630 | Placeholders |
| B8 | Confirmar 2 aliados ilegibles en el afiche (sello circular rojo/negro; "Tecnológico Loja") | `contenido/evento.yaml → aliados` |

## C. Contenido 2026

| # | Pendiente | Dónde |
|---|---|---|
| C1 | Conferencista magistral: nombre, foto, reseña (se sabe: expositor francés, "Tecnologías inmersivas y videojuegos") | `contenido/ponentes.yaml` (edición 2026) y `paginas/ponentes.yaml` |
| C2 | Ponentes de VRDay Talks (docentes y estudiantes) | `contenido/ponentes.yaml` |
| C3 | La agenda es **tentativa**: confirmar horarios definitivos; ¿habrá otras sedes LATAM además de Ecuador? | `paginas/agenda.yaml` (admite varias sedes) |
| C4 | Texto provisional "Pronto anunciaremos a los ponentes del VR Day LATAM 2026." — validar redacción | `paginas/ponentes.yaml` |
| C5 | ¿La premiación del viernes corresponde a los artículos/proyectos postulados? Si es así, explicarlo en la convocatoria | `evento.yaml → convocatorias` |
| C6 | Redes sociales oficiales y texto legal del pie | `contenido/sitio.yaml → pie` |

## D. Contenido heredado (ver detalle en `06-problemas-de-contenido.md`)

| # | Pendiente |
|---|---|
| D1 | Definiciones de RV y RA intercambiadas en *Acerca de* (error de hecho) |
| D2 | 16 reseñas de ponentes vacías (2023 y 2020) |
| D3 | 3 videos vacíos en Memorias 2021; botón "Descargar manuales" sin archivo |
| D4 | Horas incoherentes en la Agenda 2023 (ahora en memorias) |
| D5 | Plataforma inmersiva y Centro de ayuda describen 2020 (movidas al pie); actualizar o marcar como archivo |
| D6 | Erratas y nombres por confirmar (Mohamenth/Mohammad, Cuasapas/Guaspa, etc.) |
| D7 | Correo personal en la reseña de Fabian Bonilla: confirmar publicación |

## E. Decisiones técnicas y de publicación

| # | Pendiente |
|---|---|
| E1 | Google Form de contacto (URL en `paginas/contacto.yaml`) |
| E2 | ¿Mantener Google Tag Manager / Analytics? |
| E3 | Hosting destino (servidor UTPL, GitHub Pages, Netlify, Cloudflare Pages) — define cómo se publican las redirecciones |
| E4 | ¿Conservar las 3 páginas heredadas ocultas o retirarlas? |
| E5 | Confirmar URLs de memorias y redirecciones (`01 §5`) |
| E6 | **Orden de construcción:** ¿publicar primero solo el Inicio 2026 (por el plazo del 15-oct, ver A4) o seguir el orden normal del plan? |
| E7 | **Tipografía para textos largos:** solo Poppins (recomendado) o Poppins + Inter |

## F. Hecho

- [x] Repositorio git iniciado (rama `main`) con `.gitignore` y `.gitattributes`
- [x] Entorno virtual `.venv` con dependencias fijadas (`requirements.txt`, `requirements-dev.txt`)
