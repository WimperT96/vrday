from django.shortcuts import render

from . import contenido


def pagina(request, ruta=""):
    """Vista única: cualquier URL definida en contenido/paginas/*.yaml."""
    url = "/" + ruta.strip("/") + "/" if ruta.strip("/") else "/"
    datos = contenido.cargar()
    if url in datos.redirecciones:
        return redireccion(request, url)
    p = contenido.pagina(url)
    return render(request, "pagina.html", {"pagina": p})


def redireccion(request, url):
    """Página HTML de redirección (el sitio estático no puede enviar 301 reales)."""
    destino = contenido.cargar().redirecciones[url]
    return render(request, "redireccion.html", {"destino": destino, "origen": url})


def sitemap(request):
    datos = contenido.cargar()
    urls = [
        url for url, p in sorted(datos.paginas.items())
        if p.get("estado", "publicada") == "publicada"
    ]
    return render(
        request, "sitemap.xml",
        {"urls": urls, "dominio": datos.sitio["sitio"]["dominio"].rstrip("/")},
        content_type="application/xml",
    )


def robots(request):
    dominio = contenido.cargar().sitio["sitio"]["dominio"].rstrip("/")
    return render(request, "robots.txt", {"dominio": dominio}, content_type="text/plain")


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def pagina_404(request):
    """Versión exportable (status 200) de la página 404 para el hosting estático."""
    return render(request, "404.html")

