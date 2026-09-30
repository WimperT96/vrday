"""
Valida la carpeta contenido/:
  - que todos los .yaml se puedan leer,
  - que toda imagen/video referenciado exista en medios/,
  - que las URLs internas apunten a una página existente (o a una redirección),
  - lista los campos marcados como PENDIENTE y las secciones placeholder.

Uso:  python referencias/herramientas/validar_contenido.py
Se puede reutilizar tal cual como comando de Django más adelante.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENIDO = ROOT / "contenido"
MEDIOS = ROOT / "medios"
EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp|mp4|webm|glb|gltf)$", re.I)

errores, avisos = [], []
urls_paginas, urls_internas = set(), []


def recorrer(nodo, archivo, ruta=""):
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k == "carpeta" and isinstance(v, str):
                if not (MEDIOS / v).is_dir():
                    errores.append(f"{archivo}: carpeta inexistente medios/{v}")
            recorrer(v, archivo, f"{ruta}.{k}")
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            recorrer(v, archivo, f"{ruta}[{i}]")
    elif isinstance(nodo, str):
        if EXT.search(nodo) and not nodo.startswith(("http", "//")):
            if not (MEDIOS / nodo).exists():
                errores.append(f"{archivo}: no existe medios/{nodo}  ({ruta})")
        elif nodo.startswith("/") and not nodo.startswith("//") and ruta.endswith("url"):
            urls_internas.append((archivo, nodo.split("#")[0]))


archivos = sorted(CONTENIDO.rglob("*.yaml"))
datos = {}
for f in archivos:
    try:
        datos[f] = yaml.safe_load(f.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        errores.append(f"{f.relative_to(ROOT)}: YAML inválido -> {e}")

redirecciones = {}
for f, d in datos.items():
    rel = f.relative_to(ROOT)
    if isinstance(d, dict) and d.get("url"):
        urls_paginas.add(d["url"])
    if isinstance(d, dict) and "redirecciones" in d:
        redirecciones = d["redirecciones"] or {}
    recorrer(d, rel)
    texto = f.read_text(encoding="utf-8")
    for n, linea in enumerate(texto.splitlines(), 1):
        if "PENDIENTE" in linea:
            avisos.append(f"{rel}:{n}  {linea.strip()[:110]}")

for archivo, url in urls_internas:
    if url not in urls_paginas and url not in redirecciones:
        errores.append(f"{archivo}: enlace interno sin página -> {url}")

ponentes = datos.get(CONTENIDO / "ponentes.yaml", {}).get("ponentes", [])
claves = [(p["edicion"], p["slug"]) for p in ponentes]
for c in {c for c in claves if claves.count(c) > 1}:
    errores.append(f"ponentes.yaml: slug repetido en la misma edición -> {c}")

print(f"Archivos YAML: {len(archivos)}   Páginas: {len(urls_paginas)}   Ponentes: {len(ponentes)}")
print(f"\nPENDIENTES ({len(avisos)}):")
for a in avisos:
    print("  -", a)
print(f"\nERRORES ({len(errores)}):")
for e in errores:
    print("  x", e)
sys.exit(1 if errores else 0)
