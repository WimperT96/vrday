# 11. Compatibilidad con WordPress

El dominio **vrdaylatam.org** está en **GoDaddy Managed WordPress** (plataforma `wpaas`, DNS en `domaincontrol.com`).
Ese hosting espera un WordPress. Este documento resume qué está listo en el proyecto para publicarlo ahí y los dos caminos posibles.

## 1. Lo que ya está preparado (oct-2026)

| Punto | Estado |
|---|---|
| Sitio 100 % estático, sin base de datos ni PHP | `python manage.py exportar` genera 34 páginas HTML en `dist/` |
| Peso total liviano (límites de carga de WordPress) | **10,4 MB** con imágenes y video (antes ~45 MB). Imágenes en WebP con `referencias/herramientas/optimizar_medios.py` |
| Sin dependencias externas al cargar | Poppins alojada en `static/fonts/` (antes Google Fonts). Solo YouTube y Google Maps se cargan desde fuera, dentro de sus reproductores |
| Estáticos en cualquier ruta | `VR_STATIC_URL` publica CSS, JS, fuentes e imágenes en otra ruta, p. ej. la carpeta de un tema, con las páginas en la raíz. `test_estaticos_en_otra_ruta` lo cubre |
| Rutas internas sin `/` fijo en las plantillas | Todo pasa por `{% ruta %}`, `{% enlace %}`, `{% medio %}`, `{% img %}` y `{% estatico %}` |
| Caché del navegador | CSS y JS llevan `?v=<huella>`: tras cada actualización se descargan solos, sin Ctrl+F5 |
| Formularios | Ninguno propio: inscripción y postulación son enlaces externos (Google Forms, Queyam) |

Exportación lista para un tema de WordPress (en PowerShell):

```powershell
$env:VR_STATIC_URL="/wp-content/themes/vrday/static"; .venv\Scripts\python.exe manage.py exportar
Remove-Item Env:VR_STATIC_URL
```

En Git Bash, anteponer `MSYS_NO_PATHCONV=1` (si no, convierte la ruta en una ruta de Windows).
Resultado: páginas en `dist/<ruta>/index.html` y estáticos en `dist/wp-content/themes/vrday/static/`.

## 2. Camino A — Tema "contenedor" (rápido, ~medio día)

WordPress sigue instalado, como exige el hosting, pero un tema mínimo entrega las páginas ya generadas.

```
wp-content/themes/vrday/
├── style.css        cabecera obligatoria del tema (Theme Name: VR Day LATAM)
├── index.php        toma la ruta pedida (/agenda/) y devuelve paginas/agenda/index.html;
│                    si no existe, paginas/404.html con estado 404
├── paginas/         contenido de dist/ (sin la carpeta wp-content)
└── static/          contenido de dist/wp-content/themes/vrday/static/
```

- Se instala y actualiza subiendo un `.zip` en *Apariencia › Temas › Añadir › Subir tema*, sin FTP.
- El contenido se sigue editando en `contenido/*.yaml` y se vuelve a exportar.
- Las redirecciones de URLs antiguas siguen funcionando (son páginas HTML con meta refresh).
- Pendiente de construir: un comando que arme el `.zip` (`index.php`, `style.css`, `paginas/`, `static/`).

## 3. Camino B — Tema nativo editable desde el panel (2–4 semanas)

Cada componente pasa a ser un bloque o una plantilla de WordPress, y el contenido se migra al panel.

| Proyecto actual | Equivalente en WordPress |
|---|---|
| `contenido/paginas/*.yaml` (una página = un archivo) | Páginas de WordPress con bloques |
| `templates/components/<tipo>.html` (31 tipos de sección) | Bloques propios o *patterns* del tema |
| `contenido/ponentes.yaml` | Tipo de contenido "Ponente" (foto, reseña, edición, país) |
| `paginas/agenda.yaml` → `agenda_dias` | Tipo de contenido "Sesión" o un bloque de agenda |
| `contenido/evento.yaml` (fechas, lema, inscripción, aliados) | Página de opciones del tema |
| `contenido/sitio.yaml` (menú, pie, redes) | Menús de WordPress y personalizador |
| `static/css/*.css`, `static/js/main.js` | Se reutilizan tal cual en el tema |
| `templates/components/ilustraciones/*.html`, `_red_nodos.html` | SVG en línea dentro de los bloques |
| `medios/` | Biblioteca de medios |

Ventaja: el equipo edita sin depender de nadie técnico. Costo: se pierde el flujo actual (YAML, validador,
tests, publicación automática) y hay que mantener WordPress, el tema y los plugins actualizados.
