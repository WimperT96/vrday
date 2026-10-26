"""
Optimiza medios/ para la web y deja el sitio liviano (también para subirlo a un hosting
WordPress con límite de carga).

  python referencias/herramientas/optimizar_medios.py            # simula: muestra qué haría
  python referencias/herramientas/optimizar_medios.py --aplicar  # convierte y actualiza referencias

Qué hace:
1. Convierte PNG/JPG a WebP, reduciendo el lado mayor según el uso (ver REGLAS).
   Conserva la transparencia. Si el WebP no ahorra al menos 5 %, deja el original.
2. Reemplaza las rutas viejas por las nuevas en contenido/, templates/ y static/.
3. Mueve los medios sin uso a referencias/medios-sin-uso/ (no se publican, no se pierden).
   "Sin uso" = la ruta no aparece fuera de comentarios en contenido/, templates/ o static/,
   ni su carpeta se lista con `carpeta:` en una galería.
Los originales de la migración siguen en referencias/originales/.
"""
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
MEDIOS = RAIZ / "medios"
SIN_USO = RAIZ / "referencias" / "medios-sin-uso"
APLICAR = "--aplicar" in sys.argv

# (prefijo de carpeta, lado mayor máximo en px). Gana el primer prefijo que coincida.
REGLAS = [
    ("ponentes/", 600),          # círculo ~150 px y ficha ~300 px (×2 para pantallas retina)
    ("aliados/", 600),
    ("patrocinadores/", 600),
    ("marca/", 600),
    ("banderas/", 160),
    ("inicio/estadisticas/", 256),
    ("fondos/", 2560),
    ("", 1600),                  # resto: fotos de galería, cabeceras, tarjetas
]
# Se dejan como están: la imagen para compartir en redes va en JPG porque no todas las
# plataformas muestran WebP en la vista previa de enlaces.
CONSERVAR = ("marca/compartir-",)
CALIDAD_FOTO = 80
CALIDAD_TRANSPARENCIA = 88
EXT_RASTER = {".png", ".jpg", ".jpeg"}


def lado_maximo(rel: str) -> int:
    return next(m for prefijo, m in REGLAS if rel.startswith(prefijo))


def archivos_de_referencia():
    for carpeta, patrones in (("contenido", ["*.yaml"]), ("templates", ["*.html"]), ("static", ["*.css", "*.js"])):
        for patron in patrones:
            yield from (RAIZ / carpeta).rglob(patron)


def texto_sin_comentarios(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    if p.suffix == ".yaml":
        t = "\n".join(re.sub(r"(^|\s)#.*$", "", linea) for linea in t.splitlines())
    return t


def usos():
    texto = "\n".join(texto_sin_comentarios(p) for p in archivos_de_referencia())
    carpetas = set(re.findall(r"carpeta:\s*([^\s#]+)", texto))
    return texto, carpetas


def tiene_transparencia(im: Image.Image) -> bool:
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        alfa = im.convert("RGBA").getchannel("A")
        return alfa.getextrema()[0] < 255
    return False


def convertir(f: Path, rel: str):
    with Image.open(f) as im:
        if getattr(im, "is_animated", False):
            return None
        alfa = tiene_transparencia(im)
        im = im.convert("RGBA" if alfa else "RGB")
        maximo = lado_maximo(rel)
        if max(im.size) > maximo:
            im.thumbnail((maximo, maximo), Image.LANCZOS)
        destino = f.with_suffix(".webp")
        if destino.exists() and destino != f:
            return None                       # no pisar un .webp que ya existe
        tmp = destino.with_suffix(".tmp.webp")
        im.save(tmp, "WEBP", quality=CALIDAD_TRANSPARENCIA if alfa else CALIDAD_FOTO, method=6)
        return tmp, destino, im.size


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # consola de Windows (cp1252)
    texto, carpetas = usos()
    cambios, total_antes, total_despues, movidos = {}, 0, 0, []
    for f in sorted(MEDIOS.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(MEDIOS).as_posix()
        usado = rel in texto or f.parent.relative_to(MEDIOS).as_posix() in carpetas
        if not usado:
            movidos.append(rel)
            if APLICAR:
                (SIN_USO / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), SIN_USO / rel)
            continue
        if f.suffix.lower() not in EXT_RASTER or rel.startswith(CONSERVAR):
            continue
        r = convertir(f, rel)
        if not r:
            continue
        tmp, destino, tam = r
        antes, despues = f.stat().st_size, tmp.stat().st_size
        if despues > antes * 0.95:
            tmp.unlink()
            continue
        total_antes += antes
        total_despues += despues
        nuevo = destino.relative_to(MEDIOS).as_posix()
        cambios[rel] = nuevo
        print(f"  {antes/1e3:7.0f} KB → {despues/1e3:6.0f} KB  {tam[0]}×{tam[1]}  {rel} → {Path(nuevo).name}")
        if APLICAR:
            tmp.replace(destino)
            f.unlink()
        else:
            tmp.unlink()

    print(f"\nConvertidos: {len(cambios)}  ·  {total_antes/1e6:.1f} MB → {total_despues/1e6:.1f} MB")
    print(f"Sin uso ({'movidos a referencias/medios-sin-uso/' if APLICAR else 'se moverían'}): {len(movidos)}")
    for m in movidos:
        print("  ", m)

    if APLICAR and cambios:
        # Reemplaza rutas completas (también en comentarios, para que no queden obsoletas)
        patron = re.compile("|".join(re.escape(k) for k in sorted(cambios, key=len, reverse=True)))
        for p in archivos_de_referencia():
            t = p.read_text(encoding="utf-8")
            nuevo = patron.sub(lambda m: cambios[m.group(0)], t)
            if nuevo != t:
                p.write_text(nuevo, encoding="utf-8", newline="")
                print("  referencias actualizadas:", p.relative_to(RAIZ))
    if not APLICAR:
        print("\n(simulación: ejecuta con --aplicar para hacer los cambios)")


if __name__ == "__main__":
    main()
