"""
Script de migración (uso único) — sitio actual vrdaylatam.org -> estructura nueva.

1. Copia los medios descargados (referencias/originales) a medios/ con nombres limpios.
2. Genera placeholders SVG para los medios que ya no existen en el servidor.
3. Extrae los ponentes (modales de Inicio, Agenda y Agenda 2019) a contenido/ponentes.yaml.
4. Escribe docs/anexos/inventario-medios.csv (origen -> destino -> estado).

Ejecutar desde la raíz del proyecto:  python referencias/herramientas/migrar_medios_y_ponentes.py

⚠ Uso único. Sobrescribe contenido/ponentes.yaml y medios/: NO volver a ejecutarlo después de
  editar esos archivos a mano (a partir de ahora la fuente de verdad son contenido/ y medios/).
"""
import csv, json, os, re, shutil, urllib.parse as up
from pathlib import Path

import html2text, yaml
from bs4 import BeautifulSoup
from slugify import slugify

ROOT = Path(__file__).resolve().parents[2]
ORIG = ROOT / "referencias" / "originales"
HTML = ROOT / "referencias" / "captura-sitio-actual" / "html"
MEDIOS = ROOT / "medios"
CONTENIDO = ROOT / "contenido"
ANEXOS = ROOT / "docs" / "anexos"

inventario = []  # filas del CSV


def rel_from_url(url):
    url = url.split("?")[0]
    return up.unquote(url.split("wp-content/uploads/")[1])


def copiar(origen_rel, destino, pagina, uso):
    """Copia referencias/originales/<origen_rel> -> medios/<destino>. Si falta, crea placeholder."""
    src = ORIG / origen_rel
    dst = MEDIOS / destino
    dst.parent.mkdir(parents=True, exist_ok=True)
    url = "https://vrdaylatam.org/wp-content/uploads/" + origen_rel
    if src.exists():
        shutil.copy2(src, dst)
        estado = "ok"
    else:
        dst = dst.with_suffix(".svg")
        placeholder(dst, uso)
        estado = "PLACEHOLDER (original no existe)"
    inventario.append([pagina, uso, str(dst.relative_to(MEDIOS)).replace("\\", "/"), estado, url])
    return str(dst.relative_to(MEDIOS)).replace("\\", "/")


def placeholder(path, etiqueta, w=1200, h=800):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0B1450"/><stop offset=".55" stop-color="#3A1E7A"/><stop offset="1" stop-color="#009EE2"/>
  </linearGradient></defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <rect x="24" y="24" width="{w-48}" height="{h-48}" fill="none" stroke="#FFFFFF" stroke-opacity=".35" stroke-dasharray="12 10" stroke-width="3"/>
  <text x="50%" y="46%" text-anchor="middle" font-family="Montserrat, Arial, sans-serif" font-size="44" font-weight="700" fill="#FFFFFF">PLACEHOLDER</text>
  <text x="50%" y="56%" text-anchor="middle" font-family="Montserrat, Arial, sans-serif" font-size="28" fill="#FFFFFF" fill-opacity=".85">{etiqueta}</text>
</svg>
""", encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Medios con nombre fijo (marca, fondos, inicio, páginas)
# ---------------------------------------------------------------------------
FIJOS = [
    # (origen, destino, pagina, uso)
    ("2023/10/logo-del-evento-Relidad-Virtual.png", "marca/logo-vrday-latam.png", "global", "Logo del encabezado"),
    ("2023/10/fondo-general-2.png", "fondos/fondo-general-azul.png", "global", "Fondo de pie de página y sección Ponentes"),
    ("2023/11/fondo-general@125x.png", "fondos/cabecera-paginas.png", "global", "Fondo de cabecera de páginas internas (2023)"),
    ("2020/10/agenda-encabezado.jpg", "fondos/cabecera-paginas-2020.jpg", "global", "Fondo de cabecera de páginas 2020"),
    # Inicio — slider
    ("2023/10/ARTE_VR-DAY_final-scaled.jpg", "inicio/slider/01-vrday-latam-2023.jpg", "inicio", "Slider 1 — arte principal"),
    ("2022/11/1-VR day paises2.png", "inicio/slider/01-capa-paises.png", "inicio", "Slider 1 — capa de países"),
    ("2023/11/WhatsApp-Image-2023-11-07-at-9.39.58-AM.jpeg", "inicio/slider/02-anuncio.jpg", "inicio", "Slider 2"),
    ("2023/10/ARTE_VR-DAY_game-latam-scaled.jpg", "inicio/slider/03-game-latam.jpg", "inicio", "Slider 3 — Game LATAM"),
    ("2023/10/ARTE_VR-DAY_Knock-out-scaled.jpg", "inicio/slider/04-knockout.jpg", "inicio", "Slider 4 — VR Knock Out"),
    # Inicio — estadísticas
    ("2023/10/expositores-exs.png", "inicio/estadisticas/participantes.png", "inicio", "Ícono participantes"),
    ("2023/10/expositores.png", "inicio/estadisticas/expositores.png", "inicio", "Ícono expositores"),
    ("2023/10/paises.png", "inicio/estadisticas/paises.png", "inicio", "Ícono países"),
    ("2023/10/mapa-latino-america-3-125x100_c.png", "inicio/mapa-latam.png", "inicio", "Mapa Latinoamérica"),
    # Banderas
    ("2023/10/peru.png", "banderas/peru.png", "inicio/agenda", "Bandera Perú"),
    ("2023/10/chile.png", "banderas/chile.png", "inicio/agenda", "Bandera Chile"),
    ("2023/10/Brasil.png", "banderas/brasil.png", "inicio/agenda", "Bandera Brasil"),
    ("2023/10/Bolivia.png", "banderas/bolivia.png", "inicio/agenda", "Bandera Bolivia"),
    ("2023/10/panama.png", "banderas/panama.png", "inicio", "Bandera Panamá"),
    ("2023/10/Ecuador.png", "banderas/ecuador.png", "inicio/agenda", "Bandera Ecuador"),
    ("2023/10/colombia.png", "banderas/colombia.png", "inicio/agenda", "Bandera Colombia"),
    ("2023/10/argentina.png", "banderas/argentina.png", "inicio", "Bandera Argentina"),
    # Inicio — tarjetas de actividades
    ("2023/10/red-de-aprendizaje.png", "inicio/actividades/plataforma-inmersiva.png", "inicio", "Tarjeta Plataforma inmersiva"),
    ("2023/10/stands-virtuales.png", "inicio/actividades/stands-virtuales.png", "inicio", "Tarjeta Stands virtuales"),
    ("2023/10/game.png", "inicio/actividades/vrday-game-latam.png", "inicio", "Tarjeta VRDay Game LATAM"),
    ("2023/10/arte.png", "inicio/actividades/arte-en-cuarentena.png", "inicio", "Tarjeta Arte en cuarentena"),
    ("2023/10/plataformas-inmersiva.png", "inicio/actividades/red-aprendizaje-inmersivo.png", "inicio", "Tarjeta Red de aprendizaje inmersivo"),
    # Patrocinadores (pie de página)
    ("2023/10/logo-cop.png", "patrocinadores/cop.png", "global", "Auspiciante — COP"),
    ("2023/11/Globant-White.png", "patrocinadores/globant.png", "global", "Auspiciante — Globant"),
    ("2021/11/iLRN-logo-transparent-large-01-1.png", "patrocinadores/ilrn.png", "global", "Auspiciante — iLRN"),
    ("2023/10/Recurso-Unity-226x80_c.png", "patrocinadores/unity.png", "global", "Auspiciante — Unity"),
    ("2023/10/LIBEL_ACAD_BLANCO_LETRAS.png", "patrocinadores/libel-academy.png", "global", "Auspiciante — Libel Academy"),
    # Acerca de
    ("2023/11/acerca-de-terminado.png", "acerca-de/cabecera.png", "acerca-de", "Cabecera"),
    ("2023/10/realidad-virtual-personajas-png-vectores.png", "acerca-de/personajes-rx.png", "acerca-de", "Ilustración RX"),
    # Acerca de VRD anterior
    ("2020/10/publicidad-rx-01.jpg", "acerca-de-vrd-anterior/publicidad-rx.jpg", "acerca-de-vrd-anterior", "Imagen publicitaria RX"),
    ("2020/10/logo-RX-grande.png", "acerca-de-vrd-anterior/logo-realidad-x.png", "acerca-de-vrd-anterior", "Logo Realidad X UTPL"),
    # Plataforma inmersiva
    ("2020/11/plataforma-inmersiva-pasos.png", "plataforma-inmersiva/pasos.png", "plataforma-inmersiva", "Infografía de pasos"),
    # Arte en cuarentena
    ("2020/11/arte-desde-computador.jpg", "arte-en-cuarentena/como-interactuar-computador.jpg", "arte-en-cuarentena", "Instrucciones computador"),
    ("2020/11/arte-desde-celular.jpg", "arte-en-cuarentena/como-interactuar-celular.jpg", "arte-en-cuarentena", "Instrucciones celular"),
    # iLRN
    ("2020/10/red-aprendizaje-inmersivo-encabezado.jpg", "red-aprendizaje-inmersivo/cabecera.jpg", "red-de-aprendizaje-inmersivo-ilrn-ecuador", "Imagen principal"),
    # Juego Knockout
    ("2022/11/2-logo Vr Knockout-300x273.png", "juego-knockout/logo.png", "juego-knockout", "Logo VR Knock Out"),
    ("2021/11/game-300x212.png", "juego-knockout/como-jugar.png", "juego-knockout", "Ilustración ¿Cómo jugar?"),
    ("2021/11/winer-300x183.png", "juego-knockout/premios.png", "juego-knockout", "Ilustración premios"),
    # Juego Cuidémonos
    ("2020/11/CUIDEMONOS-PLAY-UTPL.mp4", "juego-cuidemonos/video-cuidemonos-play-utpl.mp4", "juego-cuidemonos-play-utpl", "Video del juego"),
    ("2020/10/gafas-realidad-virtual.jpg", "juego-cuidemonos/premio-gafas.jpg", "juego-cuidemonos-play-utpl", "Premio gafas Mirage Lenovo"),
    ("2020/11/tablet.jpg", "juego-cuidemonos/premio-tablet.jpg", "juego-cuidemonos-play-utpl", "Premio tablet"),
    # Agenda 2020 (página agenda-2019)
    ("2020/10/icon-conferencias.png", "agenda-2020/icono-conferencias.png", "agenda-2019", "Ícono conferencias"),
    ("2020/10/icon-juego-covid.png", "agenda-2020/icono-juego.png", "agenda-2019", "Ícono juego"),
    # Memorias 2019
    ("2020/10/vrd-2109-afiche.jpg", "memorias/2019/00-afiche.jpg", "vrd-2019", "Afiche 2019"),
    ("2020/10/vrd-2109-ganadores.jpg", "memorias/2019/08-ganadores.jpg", "vrd-2019/vrd-2023", "Ganadores"),
    # Memorias 2020
    ("revslider/slider-home-vrd/slide-02.jpg", "memorias/2020/00-portada.jpg", "vrd-2020", "Portada 2020"),
    # Memorias 2021
    ("2022/11/organizadoresvrd2021.jpeg", "memorias/2021/00-organizadores.jpg", "vrd-2021", "Organizadores 2021"),
    # Páginas heredadas (imágenes de demo del tema: ya no existen)
    ("2020/06/banner-set1-1.jpg", "heredadas/inicio-aries/banner.jpg", "inicio-aries", "Banner líneas de investigación"),
    ("2020/06/gpg2.jpg", "heredadas/realidad-aumentada/fondo-virtopsia.jpg", "realidad-aumentada/acordeon", "Fondo sección Virtopsia"),
    ("2020/06/gpg5.jpg", "heredadas/realidad-aumentada/app-estadistica.jpg", "realidad-aumentada", "App Estadística"),
    ("2020/06/gpg6.jpg", "heredadas/realidad-aumentada/app-generica.jpg", "realidad-aumentada", "Apps / repositorios / premios"),
    ("2020/06/shop-cat-1.jpg", "heredadas/realidad-aumentada/que-es-ra.jpg", "realidad-aumentada", "Fondo ¿Qué es RA?"),
]
for member, nombre in [("member-19", "martha-agila"), ("member-06", "jennifer-samaniego"), ("member-04", "luis-rios"),
                       ("member-03", "paola-sarango"), ("member-07", "marcelo-borja"), ("member-01", "investigador")]:
    FIJOS.append((f"2020/06/{member}.jpg", f"heredadas/realidad-aumentada/equipo/{nombre}.jpg", "realidad-aumentada", f"Foto equipo — {nombre}"))

for o, d, p, u in FIJOS:
    copiar(o, d, p, u)

# Galerías numeradas
GALERIAS = {
    "plataforma-inmersiva/capturas": ["2020/11/plataforma-01.jpg", "2020/11/plataforma-02-avatar.jpg", "2020/11/plataforma-02-otra.jpg",
                                      "2020/11/plataforma-03.jpg", "2020/11/plataforma-04.jpg", "2020/11/plataforma-05.jpg",
                                      "2020/11/plataforma-06-virbela-ponencias.jpg"],
    "stands-virtuales/capturas": ["2020/11/stands-01.jpg", "2020/11/stands-03.jpg", "2020/11/stands-04.jpg",
                                  "2020/11/stands-06.jpg", "2020/11/stands-video.jpg"],
    "juego-cuidemonos/capturas": ["2020/11/01-juego-covid-utpl.jpg", "2020/11/02-juego-cuidemonos-utpl.jpg"] +
                                 [f"2020/11/{i:02d}-juego-covid-utpl.jpg" for i in range(3, 17)],
    "memorias/2019": [f"2020/10/vrd-2109-0{i}.jpg" for i in range(1, 8)],
    "memorias/2020": [f"2021/10/Captura{i}.png" for i in (2, 3, 6, 5, 9, 7, 4, 8, 10, 11, 12, 13)],
    "memorias/2021": [f"2022/11/{i}.png" for i in (17, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12)],
    "memorias/2022": ["2023/11/WhatsApp-Image-2023-11-01-at-11.15.40-PM-1.jpeg", "2023/11/WhatsApp-Image-2023-11-01-at-11.05.08-PM.jpeg",
                      "2023/11/WhatsApp-Image-2023-11-01-at-11.01.22-PM-2.jpeg", "2023/11/WhatsApp-Image-2023-11-01-at-11.01.21-PM.jpeg",
                      "2023/11/WhatsApp-Image-2023-11-01-at-11.15.40-PM.jpeg", "2023/11/WhatsApp-Image-2023-11-01-at-11.01.22-PM.jpeg",
                      "2023/11/WhatsApp-Image-2023-11-01-at-11.05.54-PM.jpeg"],
}
galerias_out = {}
for carpeta, lista in GALERIAS.items():
    galerias_out[carpeta] = []
    for i, o in enumerate(lista, 1):
        ext = Path(o).suffix.lower().replace(".jpeg", ".jpg")
        galerias_out[carpeta].append(copiar(o, f"{carpeta}/{i:02d}{ext}", carpeta.split("/")[0], f"Galería {carpeta} #{i}"))

# ---------------------------------------------------------------------------
# 2. Ponentes (modales)
# ---------------------------------------------------------------------------
h2t = html2text.HTML2Text(); h2t.body_width = 0


def limpiar(t):
    t = re.sub(r"[*#]+", "", t)
    return re.sub(r"[ \t]+", " ", t).strip()


def modales(pagina):
    s = BeautifulSoup((HTML / f"{pagina}.html").read_text(encoding="utf-8"), "lxml")
    out = []
    for sec in s.find_all("section", class_="zn_section--inlinemodal"):
        img = sec.find("img")
        if not img:
            continue
        lineas = [limpiar(l) for l in h2t.handle(str(sec)).splitlines()]
        lineas = [l for l in lineas if l and not l.startswith("![")]
        nombre = lineas[0] if lineas else ""
        inst, resena = "", []
        for l in lineas[1:]:
            if l.lower().startswith("institución"):
                inst = l.split(":", 1)[1].strip() if ":" in l else ""
            else:
                resena.append(re.sub(r"^Reseña:\s*", "", l))
        resena = "\n\n".join(r for r in resena if r)
        out.append({"id_modal": sec.get("id"), "foto_url": img.get("src"), "nombre": nombre,
                    "institucion": inst, "resena": resena})
    return out


def orden_tarjetas(pagina):
    """Fotos de ponentes que aparecen como tarjeta visible (fuera de los modales), en orden de aparición."""
    s = BeautifulSoup((HTML / f"{pagina}.html").read_text(encoding="utf-8"), "lxml")
    modales_ = s.find_all("section", class_="zn_section--inlinemodal")
    fotos_modal = {m.find("img").get("src") for m in modales_ if m.find("img")}
    for m in modales_:
        m.decompose()
    orden = []
    for img in s.find_all("img"):
        src = img.get("src")
        if src in fotos_modal and src not in orden:
            orden.append(src)
    return orden


fuentes = {"inicio": modales("inicio"), "agenda": modales("agenda"), "agenda-2019": modales("agenda-2019")}
por_foto = {}
for pagina, lista in fuentes.items():
    for m in lista:
        por_foto.setdefault(m["foto_url"], []).append((pagina, m))

orden_inicio = orden_tarjetas("inicio")
orden_agenda = orden_tarjetas("agenda")
orden_2020 = orden_tarjetas("agenda-2019")
paises = {"colombia", "perú", "peru", "brasil", "ecuador", "chile", "bolivia", "méxico", "mexico", "argentina"}

# Erratas del Inicio que están bien escritas en otra página del sitio (Agenda o la propia reseña)
NOMBRES_CORREGIDOS = {
    "Alicia Gabirela Paredes": "Alicia Gabriela Paredes",
    "José Owsaldo Guamán": "José Oswaldo Guamán",
    "Milton Salcan": "Milton Sancán",
}

ponentes = []
for foto, variantes in por_foto.items():
    rel = rel_from_url(foto)
    edicion = 2023 if rel.startswith("2023/") else 2021 if rel.startswith("2021/") else 2020
    if rel == "2020/10/Martha-Agila.jpg" and any(p != "agenda-2019" for p, _ in variantes):
        edicion = 2023  # reutilizada en 2023 y 2020
    # Nombre: preferir el del inicio; reseña/institución: la más completa
    nombre = next((m["nombre"] for p, m in variantes if p == "inicio"), variantes[0][1]["nombre"])
    nombre_original = nombre
    nombre = NOMBRES_CORREGIDOS.get(nombre, nombre)
    resena = max((m["resena"] for _, m in variantes), key=len)
    # Texto mezclado por error en el Inicio (la versión de la Agenda está bien)
    resena = resena.replace("Artista y profesor de la UniversiIngeniero de Soporte", "Ingeniero de Soporte")
    insts = [m["institucion"] for _, m in variantes if m["institucion"]]
    inst = max(insts, key=len) if insts else ""
    pais = inst if inst.lower().strip("() ") in paises else ""
    institucion = "" if pais else inst
    slug = slugify(nombre) or slugify(Path(rel).stem)
    ext = Path(rel).suffix.lower().replace(".jpeg", ".jpg")
    base = {"slug": slug, "nombre": nombre}
    notas = []
    if nombre != nombre_original:
        notas.append(f"Nombre corregido; en el Inicio del sitio actual aparece como '{nombre_original}'.")
    variantes_nombre = sorted({m["nombre"] for _, m in variantes} - {nombre})
    if variantes_nombre:
        notas.append("Otras grafías en el sitio actual: " + ", ".join(variantes_nombre))
    if len(resena) < 25:
        notas.append("Reseña vacía o incompleta en el sitio actual — completar.")
    if len({m["resena"] for _, m in variantes}) > 1:
        notas.append("La reseña difiere entre páginas; se conservó la versión más completa.")
    ediciones_foto = [edicion]
    if rel == "2020/10/Martha-Agila.jpg":
        ediciones_foto = sorted({2023 if p != "agenda-2019" else 2020 for p, _ in variantes})
    for ed in ediciones_foto:
        destino = copiar(rel, f"ponentes/{ed}/{slug}{ext}", "/".join(sorted({p for p, _ in variantes})), f"Foto ponente {nombre} ({ed})")
        visibles = {
            2023: foto in orden_inicio,
            2021: foto in orden_agenda,
            2020: foto in orden_2020,
        }[ed]
        ponentes.append({
            **base,
            "edicion": ed,
            "pais": pais.strip("() ").title() if pais else "",
            "institucion": institucion,
            "foto": destino,
            "resena": resena,
            "visible_en_sitio_actual": visibles,
            "orden": (orden_inicio.index(foto) + 1) if ed == 2023 and foto in orden_inicio
                     else (orden_2020.index(foto) + 1) if ed == 2020 and foto in orden_2020 else 999,
            "notas": " ".join(notas),
        })

ponentes.sort(key=lambda p: (-p["edicion"], p["orden"], p["nombre"]))
for p in ponentes:
    if p["orden"] == 999:
        p.pop("orden")
    if not p["notas"]:
        p.pop("notas")


class Dumper(yaml.SafeDumper):
    pass


def str_presenter(dumper, data):
    if "\n" in data or len(data) > 90:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, str_presenter)

CONTENIDO.mkdir(exist_ok=True)
cabecera = ("# Ponentes de todas las ediciones.\n"
            "# Fuente: modales de Inicio, Agenda y Agenda 2019 del sitio actual (unificados por foto).\n"
            "# Para agregar un ponente copia un bloque, cambia 'slug' (único por edición) y la foto en medios/ponentes/<edicion>/.\n"
            "# visible_en_sitio_actual=false -> existía en el sitio pero sin tarjeta visible (modal huérfano).\n\n")
with open(CONTENIDO / "ponentes.yaml", "w", encoding="utf-8") as f:
    f.write(cabecera)
    yaml.dump({"ponentes": ponentes}, f, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=1000)

ANEXOS.mkdir(parents=True, exist_ok=True)
with open(ANEXOS / "inventario-medios.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pagina", "uso", "archivo_nuevo (medios/)", "estado", "url_original"])
    w.writerows(sorted(inventario, key=lambda r: (r[0], r[2])))

print("ponentes:", len(ponentes), {e: sum(1 for p in ponentes if p["edicion"] == e) for e in (2023, 2021, 2020)})
print("medios:", len(inventario), "placeholders:", sum(1 for r in inventario if r[3] != "ok"))
