"""
Cargador de contenido: lee contenido/*.yaml y prepara los datos que usan las plantillas.

- Todo el contenido se cachea en memoria y se recarga solo si algún .yaml cambió
  (se comparan fechas de modificación), así que en desarrollo basta con guardar el archivo.
- Las secciones con `fuente:` (evento, agenda) y las de tipo `ponentes` / `galeria`
  se "resuelven" aquí para que las plantillas no tengan lógica.
"""
import copy
import datetime
import threading
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from django.conf import settings
from django.http import Http404

EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

_bloqueo = threading.Lock()
_cache = {"firma": None, "datos": None}


@dataclass
class Datos:
    sitio: dict
    evento: dict
    ponentes: list
    paginas: dict = field(default_factory=dict)       # url -> página (sin resolver)
    redirecciones: dict = field(default_factory=dict)  # url antigua -> url nueva


def _leer(ruta: Path):
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _firma(base: Path):
    return tuple(sorted((str(p), p.stat().st_mtime_ns) for p in base.rglob("*.yaml")))


def _normalizar_url(url: str) -> str:
    if not url.startswith("/"):
        url = "/" + url
    if not url.endswith("/"):
        url += "/"
    return url


def cargar() -> Datos:
    """Devuelve todo el contenido (cacheado; se recarga si cambió algún YAML)."""
    base = Path(settings.CONTENIDO_DIR)
    firma = _firma(base)
    with _bloqueo:
        if _cache["firma"] == firma and _cache["datos"] is not None:
            return _cache["datos"]
        sitio = _leer(base / "sitio.yaml")
        evento = _leer(base / "evento.yaml")
        # Organizadores/aliados con `publicar: false` quedan en el YAML pero no se muestran.
        for clave in ("organizadores", "aliados"):
            evento[clave] = [x for x in evento.get(clave) or [] if x.get("publicar", True) is not False]
        datos = Datos(
            sitio=sitio,
            evento=evento,
            ponentes=_leer(base / "ponentes.yaml").get("ponentes", []),
            redirecciones={
                _normalizar_url(k): v for k, v in (sitio.get("redirecciones") or {}).items()
            },
        )
        for archivo in sorted((base / "paginas").rglob("*.yaml")):
            pagina = _leer(archivo)
            if not pagina.get("url"):
                continue
            pagina["_archivo"] = str(archivo.relative_to(base))
            datos.paginas[_normalizar_url(pagina["url"])] = pagina
        _cache.update(firma=firma, datos=datos)
        return datos


def url_sitio(url):
    """Antepone la subcarpeta de publicación (settings.SITIO_BASE) a las rutas internas."""
    base = getattr(settings, "SITIO_BASE", "")
    if base and isinstance(url, str) and url.startswith("/") and not url.startswith("//"):
        return base + url
    return url


def urls_paginas(incluir_ocultas=True):
    datos = cargar()
    return [
        url for url, p in datos.paginas.items()
        if incluir_ocultas or p.get("estado", "publicada") == "publicada"
    ]


def valor(datos: Datos, ruta: str):
    """Resuelve rutas tipo 'evento.inscripcion.url' sobre el contenido."""
    partes = ruta.split(".")
    raiz = {"evento": datos.evento, "sitio": datos.sitio}.get(partes[0])
    for parte in partes[1:]:
        if not isinstance(raiz, dict):
            return None
        raiz = raiz.get(parte)
    return raiz


# ── Resolución de secciones ─────────────────────────────────────────────────

def _hoy():
    return datetime.date.today()


def _ponentes(datos, s):
    lista = [p for p in datos.ponentes if p.get("edicion") == s.get("edicion")]
    if s.get("solo_visibles"):
        lista = [p for p in lista if p.get("visible_en_sitio_actual", True)]
    return sorted(lista, key=lambda p: (p.get("orden", 999), p.get("nombre", "")))


def _galeria(s):
    if s.get("carpeta"):
        carpeta = Path(settings.MEDIOS_DIR) / s["carpeta"]
        archivos = sorted(p for p in carpeta.iterdir() if p.suffix.lower() in EXT_IMAGEN)
        return [{"src": f"{s['carpeta']}/{p.name}", "alt": ""} for p in archivos]
    imagenes = []
    for img in s.get("imagenes") or []:
        imagenes.append(img if isinstance(img, dict) else {"src": img, "alt": ""})
    return imagenes


# Red de nodos de la banda "Un evento que conecta" (protagonista de la sección).
# Dos capas: "ancha" (lienzo 1120×460, centro 560,230) y "compacta" para móvil
# (360×540, centro 180,270). Cada nodo: posición, lado de la etiqueta, desplazamiento
# horizontal de la etiqueta en móvil y trazo tipo circuito que sale del centro.
# Hay 4 posiciones; si el YAML trae más palabras, se usan las 4 primeras.
_RED_CAPAS = {
    "ancha": ((1120, 460), [
        {"x": 230, "y": 96, "lado": "arriba", "ruta": "M527 197 L470 140 V96 H230"},
        {"x": 900, "y": 120, "lado": "arriba", "ruta": "M593 197 L640 150 H760 L790 120 H900"},
        {"x": 960, "y": 360, "lado": "abajo", "ruta": "M593 263 L640 310 V360 H960"},
        {"x": 170, "y": 340, "lado": "abajo", "ruta": "M514 230 H400 L320 310 V340 H170"},
    ]),
    "compacta": ((360, 540), [
        # Alturas escalonadas para que las etiquetas no se monten en pantallas de 360 px.
        {"x": 64, "y": 100, "lado": "arriba", "ancla": "-18%", "ruta": "M154 244 L120 210 V100 H64"},
        {"x": 296, "y": 175, "lado": "arriba", "ancla": "-82%", "ruta": "M206 244 L240 210 V175 H296"},
        {"x": 296, "y": 445, "lado": "abajo", "ancla": "-82%", "ruta": "M206 296 L240 330 V445 H296"},
        {"x": 64, "y": 375, "lado": "abajo", "ancla": "-18%", "ruta": "M154 296 L120 330 V375 H64"},
    ]),
}


def _red_nodos(nodos):
    """`nodos` admite palabras sueltas o {texto, icono}."""
    red = []
    for i, nodo in enumerate(nodos[:4]):
        nodo = nodo if isinstance(nodo, dict) else {"texto": nodo}
        item = {"texto": nodo.get("texto", ""), "icono": nodo.get("icono", "")}
        for capa, ((ancho, alto), posiciones) in _RED_CAPAS.items():
            n = posiciones[i]
            # Como texto: un float se localizaría con coma decimal ("19,64") y rompería el CSS.
            item[capa] = {**n, "x_pct": f"{n['x'] / ancho * 100:.2f}", "y_pct": f"{n['y'] / alto * 100:.2f}"}
        red.append(item)
    return red


def _agenda_dias(datos):
    agenda = datos.paginas.get("/agenda/", {})
    for s in agenda.get("secciones", []):
        if s.get("tipo") == "agenda_dias":
            return s
    return {}


def resolver_seccion(datos: Datos, s: dict) -> dict:
    s = copy.deepcopy(s)
    tipo = s.get("tipo")
    fuente = s.get("fuente")

    if tipo == "ponentes":
        s["lista"] = _ponentes(datos, s)
    elif tipo == "galeria":
        s["imagenes"] = _galeria(s)
    elif tipo == "banda" and s.get("nodos"):
        s["red"] = _red_nodos(s["nodos"])
    elif tipo in ("hero_evento", "aliados", "inscripcion"):
        s["evento"] = datos.evento
        ini = (datos.evento.get("fechas") or {}).get("inicio")
        fin = (datos.evento.get("fechas") or {}).get("fin") or ini
        if isinstance(ini, datetime.date) and isinstance(fin, datetime.date):
            # Banda de fecha como en la maqueta: "12 y 13 de" / "noviembre de 2026"
            dias = f"{ini.day} y {fin.day}" if fin != ini else f"{ini.day}"
            s["fecha_dias"] = f"{dias} de"
            s["fecha_mes"] = f"{MESES[ini.month - 1]} de {ini.year}"
    elif tipo == "caracteristicas":
        s["items"] = s.get("items") or valor(datos, fuente or "evento.caracteristicas") or []
    elif tipo == "convocatorias":
        items = s.get("items") or valor(datos, fuente or "evento.convocatorias") or []
        # Se ocultan las convocatorias vencidas (a la fecha de generación del sitio).
        s["items"] = [
            c for c in items
            if not isinstance(c.get("fecha_limite"), datetime.date) or c["fecha_limite"] >= _hoy()
        ]
    elif tipo == "agenda_resumen":
        agenda = _agenda_dias(datos)
        destacar = set(s.get("destacar") or [])
        dias = []
        for sede in agenda.get("sedes", []):
            for dia in sede.get("dias", []):
                sesiones = [x for x in dia.get("sesiones", []) if not destacar or x.get("actividad") in destacar]
                dias.append({"etiqueta": dia.get("etiqueta"), "sede": sede.get("nombre"), "sesiones": sesiones})
        s["dias"] = dias
        s["tentativa"] = agenda.get("tentativa", False)
    elif tipo == "agenda_dias":
        for sede in s.get("sedes", []):
            for dia in sede.get("dias", []):
                dia.setdefault("id", str(dia.get("fecha", "")))
    return s


def pagina(url: str) -> dict:
    """Página lista para renderizar (secciones resueltas). Lanza Http404 si no existe."""
    datos = cargar()
    p = datos.paginas.get(_normalizar_url(url))
    if p is None:
        raise Http404(url)
    p = copy.deepcopy(p)
    p["secciones"] = [
        resolver_seccion(datos, s) for s in p.get("secciones", []) if s.get("mostrar", True) is not False
    ]
    return p
