"""
URLs del sitio.

Todas las páginas salen de contenido/paginas/*.yaml: no hay que registrar URLs a mano.
`distill_path=True` + `distill_func` le dicen a django-distill qué páginas exportar.
(django-distill 4.x reemplaza django.urls.path al iniciar, por eso se usa `urls.path`).
"""
from django import urls

from sitio import contenido, views


def _rutas_paginas():
    """Parámetros para exportar cada página y cada redirección (menos el Inicio)."""
    datos = contenido.cargar()
    rutas = [u.strip("/") for u in datos.paginas if u != "/"]
    rutas += [u.strip("/") for u in datos.redirecciones]
    return [{"ruta": r} for r in sorted(set(rutas))]


urlpatterns = [
    urls.path("", views.pagina, name="inicio", distill_path=True, distill_file="index.html"),
    urls.path("sitemap.xml", views.sitemap, name="sitemap", distill_path=True),
    urls.path("robots.txt", views.robots, name="robots", distill_path=True),
    urls.path("404.html", views.pagina_404, name="pagina-404", distill_path=True),
    urls.path(
        "<path:ruta>/", views.pagina, name="pagina",
        distill_path=True, distill_func=_rutas_paginas,
    ),
]

handler404 = "sitio.views.error_404"
