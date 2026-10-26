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
| A1 | **Sede 2026 — detalles para la página "Lugar"**: dirección exacta, fotos, indicaciones de llegada (~~mapa~~ ✅ Centro de Convenciones UTPL, 22-oct-2026) | `contenido/evento.yaml → lugar`, `contenido/paginas/lugar.yaml` | Ya se sabe: UTPL (Loja), Centro de Convenciones UTPL, stands en el Hall del Aula Magna y en el sector de ingreso al Rectorado (dato de la agenda) |
| A2 | ~~Enlace de inscripción 2026~~ ✅ Google Form (22-oct-2026) | `contenido/evento.yaml → inscripcion.url` | Activa los botones del menú, del hero y de la sección de inscripción |
| A3 | ~~Enlace de postulación de artículos~~ ✅ https://queyam.com/editorial/home/vrdlatam2026 | `contenido/evento.yaml → convocatorias[0].url` | |
| A4 | ~~Plazo de postulación~~ ✅ venció el 25-oct-2026; la convocatoria sigue visible a pedido (`mostrar_vencida: true`) | `contenido/evento.yaml → convocatorias` | |

## B. Recursos gráficos (pedir al diseñador)

| # | Recurso | Estado actual |
|---|---|---|
| B1 | Logo 2026 en SVG: ~~horizontal y versión blanca~~ ✅ sacados del .ai (`marca/logo-vrday-2026.svg` y `-blanco.svg`, 23-oct-2026); faltan apilado e isotipo | Placeholders `logo-vrday-2026-apilado.svg`, `isotipo-visor.svg` |
| B2 | Nombre/licencia de la fuente de "DAY" y "12 Y 13 DE" | — |
| B3 | ~~Foto del hero~~ ✅ el hero muestra el Short "Virtual Reality Day Latam 2026" (24-oct-2026) | `inicio.yaml → video` |
| B4 | ~~Foto de la banda navy~~ ✅ ya no hace falta: la banda usa una red de nodos animada (22-oct-2026) | La foto del afiche quedó en `medios/inicio-2026/banda-conecta.jpg`, sin usar (candidata para el hero, B3) |
| B5 | Logos individuales de UTPL, RAIN y 16 aliados | Solo existen dentro del afiche; mientras tanto se muestran los nombres |
| B6 | Patrones SVG (circuitos, hexágonos, anillos HUD) | — |
| B7 | Favicon y `apple-touch-icon` (la imagen para redes 1200×630 ✅ ya está: `marca/compartir-2026.jpg`) | Favicon: placeholder `marca/isotipo-visor.svg` |
| B8 | Confirmar 2 aliados ilegibles en el afiche (sello circular rojo/negro; "Tecnológico Loja") | `contenido/evento.yaml → aliados` |

## C. Contenido 2026

| # | Pendiente | Dónde |
|---|---|---|
| C1 | ~~Conferencista magistral~~ ✅ Vincent Moulinet (Francia), con apoyo de la Embajada de Francia en Ecuador — foto y reseña breve (22-oct-2026) | `contenido/ponentes.yaml` (edición 2026) y `paginas/ponentes.yaml` |
| C2 | Ponentes de VRDay Talks (docentes y estudiantes) | `contenido/ponentes.yaml` |
| C3 | ~~Agenda tentativa~~ ✅ agenda del PDF "Invitación a delegados" (22-oct-2026). Queda: ¿habrá otras sedes LATAM además de Ecuador? (El "Circuito" de las 16:30 es el Circuito Ciencia y Arte del FIAV, aclarado el 23-oct-2026.) | `paginas/agenda.yaml` (admite varias sedes) |
| C4 | Texto provisional "Pronto anunciaremos a los ponentes del VR Day LATAM 2026." — validar redacción | `paginas/ponentes.yaml` |
| C5 | ¿La premiación del viernes corresponde a los artículos/proyectos postulados? Si es así, explicarlo en la convocatoria | `evento.yaml → convocatorias` |
| C6 | Texto legal del pie (las redes sociales ✅ ya están: Instagram y YouTube) | `contenido/sitio.yaml → pie.texto_legal` |

## D. Contenido heredado (ver detalle en `06-problemas-de-contenido.md`)

| # | Pendiente |
|---|---|
| D1 | ~~Definiciones de RV y RA intercambiadas~~ ✅ corregido el 22-oct-2026 |
| D2 | 16 reseñas de ponentes vacías (2023 y 2020) |
| D3 | ~~3 videos vacíos en Memorias 2021~~ ✅ 2 videos de YouTube agregados (22-oct-2026); botón "Descargar manuales" sin archivo |
| D4 | Horas incoherentes en la Agenda 2023 (ahora en memorias) |
| D5 | Plataforma inmersiva y Centro de ayuda describen 2020 (movidas al pie); actualizar o marcar como archivo |
| D6 | Erratas y nombres por confirmar (Mohamenth/Mohammad, Cuasapas/Guaspa, etc.) |
| D7 | Correo personal en la reseña de Fabian Bonilla: confirmar publicación |

## E. Decisiones técnicas y de publicación

| # | Pendiente |
|---|---|
| E1 | ~~Google Form de contacto~~ — ya no aplica: la página Contacto se eliminó (22-oct-2026) |
| E2 | ¿Mantener Google Tag Manager / Analytics? |
| E3 | ~~Hosting destino~~ ✅ GitHub Pages con el dominio vrdaylatam.org (activo desde el 26-oct-2026, `docs/12-dominio-propio.md`) |
| E4 | ¿Conservar las 3 páginas heredadas ocultas o retirarlas? |
| E5 | ~~Confirmar URLs y redirecciones~~ ✅ las 20 URLs del WordPress anterior funcionan en vrdaylatam.org (revisado el 26-oct-2026) |
| E6 | ~~Orden de construcción~~ ✅ ya no aplica: el sitio completo está publicado |
| E7 | **Tipografía para textos largos:** solo Poppins (recomendado) o Poppins + Inter |

| E8 | ~~Fuentes desde Google Fonts~~ ✅ Poppins alojada en `static/fonts/` (26-oct-2026) |
| E9 | GTM/GA4 **no** están incluidos en las plantillas hasta decidir E2 |

## G. Técnicos para la fase 4 (calidad y publicación)

| # | Pendiente |
|---|---|
| G1 | ~~Optimizar imágenes~~ ✅ WebP con tamaño según el uso (26-oct-2026): `dist/` pasó de ~45 MB a 10,4 MB. Queda opcional: `srcset` con varios tamaños |
| G2 | ~~Logo del encabezado con fondo~~ ✅ SVG transparente sacado del .ai (23-oct-2026) |
| G3 | Revisión visual página por página y ajustes finos de espaciado con los recursos reales |
| G4 | Auditoría Lighthouse (rendimiento, accesibilidad, SEO) en móvil |
| G5 | ~~Redirecciones 301 reales~~ GitHub Pages no permite 301 propios: se usan páginas de redirección (meta refresh + canonical), que Google trata como permanentes ✅ |
| G6 | ~~Volver a exportar tras el plazo~~ ✅ ya no aplica (`mostrar_vencida: true`) |

## F. Hecho

- [x] Repositorio git iniciado (rama `main`) con `.gitignore` y `.gitattributes`
- [x] Entorno virtual `.venv` con dependencias fijadas (`requirements.txt`, `requirements-dev.txt`)
- [x] Sitio Django: 25 páginas, 31 componentes, identidad 2026, exportación estática, pruebas automáticas
