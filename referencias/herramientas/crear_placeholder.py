"""
Crea un placeholder SVG con la identidad 2026 (fondo claro, azul de marca, lavanda).

Uso:
  python referencias/herramientas/crear_placeholder.py <ruta en medios/> "<texto>" [ancho] [alto]
Ejemplo:
  python referencias/herramientas/crear_placeholder.py inicio-2026/hero-persona-vr.svg "Foto hero: persona con visor VR" 1200 1000
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

MEDIOS = Path(__file__).resolve().parents[2] / "medios"


def crear(ruta, texto, w=1200, h=800):
    destino = MEDIOS / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    texto = escape(texto)
    destino.write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <radialGradient id="g" cx="70%" cy="40%" r="75%">
      <stop offset="0" stop-color="#C9E0FD"/><stop offset=".5" stop-color="#E6D5F7"/><stop offset="1" stop-color="#F4F8FC"/>
    </radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <g fill="none" stroke="#4D9CF6" stroke-opacity=".35" stroke-width="2">
    <circle cx="{w*0.5}" cy="{h*0.42}" r="{min(w, h)*0.12}"/>
    <circle cx="{w*0.5}" cy="{h*0.42}" r="{min(w, h)*0.17}" stroke-dasharray="6 10"/>
  </g>
  <rect x="20" y="20" width="{w-40}" height="{h-40}" rx="20" fill="none" stroke="#4D9CF6" stroke-opacity=".6" stroke-dasharray="14 10" stroke-width="3"/>
  <text x="50%" y="{h*0.42 + 12}" text-anchor="middle" font-family="Poppins, Arial, sans-serif" font-size="{max(18, w//30)}" font-weight="700" fill="#071A38">PLACEHOLDER</text>
  <text x="50%" y="{h*0.72}" text-anchor="middle" font-family="Poppins, Arial, sans-serif" font-size="{max(14, w//45)}" fill="#4A5B78">{texto}</text>
</svg>
""", encoding="utf-8")
    return destino


if __name__ == "__main__":
    ruta, texto = sys.argv[1], sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 800
    print(crear(ruta, texto, w, h))
