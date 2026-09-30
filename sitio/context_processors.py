from django.conf import settings

from . import contenido


def _activo(ruta_actual, url):
    if not url or not url.startswith("/"):
        return False
    if url == "/":
        return ruta_actual == "/"
    return ruta_actual.startswith(url)


def sitio(request):
    """Variables disponibles en todas las plantillas: sitio, evento, menú y pie."""
    datos = contenido.cargar()
    ruta = request.path if request else "/"
    menu = []
    for item in datos.sitio.get("menu_principal", []):
        item = dict(item)
        item["activo"] = _activo(ruta, item.get("url"))
        item["submenu"] = [
            {**sub, "activo": _activo(ruta, sub.get("url"))} for sub in item.get("submenu") or []
        ]
        item["activo"] = item["activo"] or any(sub["activo"] for sub in item["submenu"])
        menu.append(item)

    boton = dict(datos.sitio.get("boton_cabecera") or {})
    if boton.get("url_desde"):
        boton["url"] = contenido.valor(datos, boton["url_desde"]) or ""

    return {
        "sitio": datos.sitio.get("sitio", {}),
        "seo_base": datos.sitio.get("seo", {}),
        "analitica": datos.sitio.get("analitica", {}),
        "menu": menu,
        "boton_cabecera": boton,
        "pie": datos.sitio.get("pie", {}),
        "evento": datos.evento,
        "mostrar_placeholders": settings.MOSTRAR_PLACEHOLDERS,
        "no_indexar": settings.NO_INDEXAR,
    }
