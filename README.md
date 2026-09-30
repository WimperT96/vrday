# VR Day Latam — nueva versión del sitio

Recopilación completa del sitio actual **https://vrdaylatam.org/** (WordPress + tema Kallyas) para reconstruirlo como **sitio estático con Django**.
Captura realizada el **30-sep-2026**.

---

## Cómo está organizado este repositorio

```
vrday/
├── README.md                ← este archivo (empieza aquí)
├── docs/                    ← decisiones, análisis y plan (leer en orden)
│   ├── 01-mapa-del-sitio.md          páginas, menú, URLs antiguas → nuevas
│   ├── 02-identidad-visual.md        identidad 2026 validada: colores, tipografía, componentes
│   ├── 03-arquitectura-django.md     cómo se construirá el sitio y cómo se edita el contenido
│   ├── 04-medios.md                  imágenes y videos: qué hay, qué falta, placeholders
│   ├── 05-enlaces-y-formularios.md   formularios → Google Forms, enlaces externos, embeds
│   ├── 06-problemas-de-contenido.md  errores, textos de relleno, datos incompletos
│   ├── 07-efectos-y-3d.md            preparación para animaciones, efectos y objetos 3D
│   ├── 08-plan-de-trabajo.md         fases y checklist para construir el sitio
│   ├── 09-pendientes.md              ← TODO lo que falta, en una sola lista
│   ├── 10-guia-de-prueba.md          paso a paso para probar la web en tu computador
│   └── anexos/inventario-medios.csv  lista completa archivo por archivo
│
├── contenido/               ← FUENTE DE VERDAD: todo el texto del sitio en YAML
│   ├── sitio.yaml                    nombre, menú, pie, auspiciantes, redirecciones
│   ├── evento.yaml                   edición 2026: fechas, lema, convocatoria, sede y aliados
│   ├── ponentes.yaml                 71 ponentes (2023, 2021, 2020) con foto y reseña
│   └── paginas/                      una página = un archivo .yaml
│       ├── inicio.yaml, acerca-de.yaml, agenda.yaml, …
│       ├── inicio.yaml, agenda.yaml  edición 2026 · ponentes.yaml, lugar.yaml (nuevas)
│       ├── memorias/                 índice + 2019 … 2023 (+ agendas 2020 y 2023, acerca de 2020)
│       └── heredadas/                páginas antiguas no enlazadas (se conservan ocultas)
│
├── medios/                  ← imágenes y videos ya renombrados y ordenados (listos para usar)
│   ├── marca/  fondos/  banderas/  patrocinadores/
│   ├── inicio/  acerca-de/  plataforma-inmersiva/  …   (una carpeta por página)
│   ├── ponentes/2023/  ponentes/2021/  ponentes/2020/
│   ├── memorias/2019 … 2022/
│   └── heredadas/           (placeholders .svg de imágenes que ya no existen)
│
└── referencias/             ← material de respaldo (no se publica)
    ├── originales/                   descargas tal cual del servidor (misma ruta que wp-content/uploads)
    ├── captura-sitio-actual/html/    HTML de cada página del sitio actual
    ├── captura-sitio-actual/texto/   el mismo contenido convertido a texto, sección por sección
    ├── identidad/                    maqueta web y afiche 2026 + descripción de la identidad
    ├── evento-2026/                  agenda tentativa 2026 (imagen original)
    └── herramientas/                 scripts de migración y validación
```

## Resumen en cifras

| | |
|---|---|
| Páginas del sitio actual | 21 páginas WordPress + 12 fichas "portfolio" de demostración |
| Páginas del sitio nuevo | **25**: 20 existentes + índice de Memorias + Memorias 2023 y su agenda (contenido 2023 reubicado) + Ponentes y Lugar (nuevas 2026); se descartan la página vacía "Prueba" y las 12 fichas demo |
| Menú | 7 entradas (maqueta 2026) + submenú Memorias (5 ediciones) + botón Inscríbete |
| Ponentes | **71** (40 de 2023, 19 de 2021, 12 de 2020) |
| Medios descargados | **187** archivos (≈ 43 MB) — todos los que aún existen |
| Medios faltantes | **11** → reemplazados por placeholders `.svg` (todas de páginas heredadas) |
| Videos de YouTube | 11 enlazados, todos disponibles · 3 reproductores vacíos en VRD 2021 |
| Formularios propios | 1 (Contacto) → se reemplaza por Google Form |

## Estado actual (30-sep-2026)

- **Sitio Django funcionando**: las 25 páginas se generan desde los YAML con la identidad 2026, y se exportan a HTML estático (`python manage.py exportar`).
- Sitio reorganizado para la **edición 2026** (12 y 13 de noviembre, UTPL): nuevo Inicio, Agenda tentativa, páginas Ponentes y Lugar, menú de la maqueta.
- Edición 2023 archivada en `/memorias/2023/`.
- Pendientes consolidados en **`docs/09-pendientes.md`**.

## Qué hacer primero

1. **Revisar `docs/09-pendientes.md`**: lista única de datos, recursos y decisiones que faltan.
2. **Identidad visual 2026** ✅ recibida y validada (`docs/02-identidad-visual.md`). Falta pedir al diseñador los recursos en vector (logo SVG, logos de aliados, foto del hero) — lista en la sección 6 de ese documento.
3. **Crear el Google Form de contacto** y pegar su URL en `contenido/paginas/contacto.yaml`.
4. Revisar la lista de **PENDIENTES** con:
   ```
   python referencias/herramientas/validar_contenido.py
   ```

## Preparar el entorno (una sola vez por equipo)

```powershell
git clone <url-del-repositorio> vrday     # o usar esta carpeta
cd vrday
python -m venv .venv
.venv\Scripts\activate                     # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt        # sitio + herramientas de migración
python referencias/herramientas/validar_contenido.py
```

- `requirements.txt`: lo que necesita el sitio (Django 5.2 LTS, django-distill, PyYAML, Markdown, Pillow), con versiones fijadas.
- `requirements-dev.txt`: lo anterior + herramientas usadas para capturar el sitio actual.
- Python 3.12. El entorno `.venv/` no se sube al repositorio.

## Ejecutar y exportar el sitio

```powershell
.venv\Scripts\activate
python manage.py runserver            # desarrollo: http://127.0.0.1:8000
python manage.py test sitio           # comprueba que todas las páginas funcionan
python manage.py exportar             # genera el sitio estático en dist/
python -m http.server 8080 --directory dist   # previsualizar lo exportado
```

Detalle de comandos: `docs/03-arquitectura-django.md §6`.

## Vista previa en GitHub Pages

Cada `push` a `main` ejecuta `.github/workflows/publicar-pages.yml`: corre las pruebas, exporta el sitio y lo publica en
`https://<usuario-u-organizacion>.github.io/<repositorio>/`.

- Se publica bajo una subcarpeta (variable `VR_BASE_URL`): todas las rutas del sitio se ajustan solas.
- Es una **vista previa**: pide a los buscadores no indexarla y muestra las marcas de "Contenido provisional".
- Configuración inicial (una sola vez): **Settings → Pages → Source: GitHub Actions**.
- Probar lo mismo en local (PowerShell):
  ```powershell
  $env:VR_BASE_URL="/vrday"; $env:VR_NOINDEX="1"; .venv\Scripts\python.exe manage.py exportar --borrador
  Remove-Item Env:VR_BASE_URL, Env:VR_NOINDEX
  ```
  En Git Bash hay que anteponer `MSYS_NO_PATHCONV=1`, porque Git Bash convierte `/vrday` en una ruta de Windows.

## Cómo editar contenido (resumen)

- Todo el texto vive en `contenido/**/*.yaml`. Cambiar un texto = editar el YAML; no hay que tocar HTML.
- Las imágenes se referencian con rutas relativas a `medios/` (p. ej. `ponentes/2023/aura-forero.png`).
  Para reemplazar un placeholder por la imagen definitiva, se guarda el archivo nuevo y se cambia la ruta.
- Después de cualquier cambio, ejecutar `validar_contenido.py`: avisa si falta una imagen o un enlace interno quedó roto.
- Detalle completo del formato: `docs/03-arquitectura-django.md` → sección "Catálogo de secciones".
