"""
Etiquetas y filtros de plantilla del sitio (disponibles en todas las plantillas sin {% load %}).

  {% medio ruta %}                    URL de un archivo de medios/
  {% img ruta alt clase carga %}      <img> con width/height, lazy loading y texto alternativo
  {% enlace url %}                    atributos href (+ target/rel si es externo; subcarpeta si es interno)
  {% ruta "/memorias/" %}             ruta interna con la subcarpeta de publicación
  {% icono "cubo" %}                  ícono SVG del sprite (templates/partials/iconos.html)
  {{ texto|md }}                      Markdown -> HTML
  {{ texto|md_linea }}                Markdown en línea (sin <p>), p. ej. "Un evento que **conecta**"
  {{ dic|a_json }}                    JSON para atributos data-*
  {{ ruta|empieza:"fondos/" }}        str.startswith
  {{ id|yt_miniatura }}               miniatura de YouTube
  {{ fecha|fecha_larga }}             12 de noviembre de 2026
"""
import datetime
import json
import re
from functools import lru_cache
from pathlib import Path

import markdown as md_lib
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

from sitio.contenido import MESES, url_sitio


@register.simple_tag
def medio(ruta):
    return static(f"medios/{ruta}") if ruta else ""


@lru_cache(maxsize=2048)
def _dimensiones(ruta_absoluta: str, _mtime: int):
    p = Path(ruta_absoluta)
    try:
        if p.suffix.lower() == ".svg":
            cabecera = p.read_text(encoding="utf-8", errors="ignore")[:600]
            w = re.search(r'\bwidth="(\d+)', cabecera)
            h = re.search(r'\bheight="(\d+)', cabecera)
            return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)
        from PIL import Image
        with Image.open(p) as im:
            return im.size
    except (OSError, ValueError):
        return (None, None)


def dimensiones(ruta):
    p = Path(settings.MEDIOS_DIR) / ruta
    if not p.exists():
        return (None, None)
    return _dimensiones(str(p), p.stat().st_mtime_ns)


@register.simple_tag
def img(ruta, alt="", clase="", carga="lazy"):
    if not ruta:
        return ""
    ancho, alto = dimensiones(ruta)
    tam = format_html(' width="{}" height="{}"', ancho, alto) if ancho and alto else ""
    return format_html(
        '<img src="{}" alt="{}" class="{}" loading="{}" decoding="async"{}>',
        medio(ruta), alt or "", clase, carga, tam,
    )


def es_externo(url):
    return bool(url) and str(url).startswith(("http://", "https://", "//"))


@register.filter
def externo(url):
    return es_externo(url)


@register.simple_tag
def enlace(url):
    if not url:
        return mark_safe('href="#" aria-disabled="true"')
    if es_externo(url):
        return format_html('href="{}" target="_blank" rel="noopener"', url)
    return format_html('href="{}"', url_sitio(url))


@register.simple_tag
def ruta(url):
    """Ruta interna con la subcarpeta de publicación: {% ruta "/memorias/" %}"""
    return url_sitio(url)


@register.simple_tag
def icono(nombre, clase=""):
    return format_html(
        '<svg class="icono {}" aria-hidden="true" focusable="false"><use href="#i-{}"></use></svg>',
        clase, nombre,
    )


class _EnlacesExternos(md_lib.treeprocessors.Treeprocessor):
    def run(self, root):
        for a in root.iter("a"):
            href = a.get("href", "")
            if es_externo(href):
                a.set("target", "_blank")
                a.set("rel", "noopener")
            else:
                a.set("href", url_sitio(href))


class _ExtEnlaces(md_lib.Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(_EnlacesExternos(md), "enlaces_externos", 5)


def _markdown(texto):
    return md_lib.markdown(str(texto or ""), extensions=["extra", "sane_lists", _ExtEnlaces()])


@register.filter
def md(texto):
    return mark_safe(_markdown(texto))


@register.filter
def md_linea(texto):
    html = _markdown(texto).strip()
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return mark_safe(html)


@register.filter
def a_json(valor):
    return json.dumps(valor or {}, ensure_ascii=False, default=str)


@register.filter
def empieza(texto, prefijo):
    return str(texto or "").startswith(prefijo)


@register.filter
def yt_miniatura(video_id):
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else ""


@register.filter
def fecha_larga(fecha):
    if isinstance(fecha, datetime.date):
        return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}"
    return fecha or ""


@register.filter
def iniciales(nombre):
    partes = [p for p in str(nombre or "").split() if p[:1].isalpha()]
    return "".join(p[0] for p in partes[:2]).upper()
