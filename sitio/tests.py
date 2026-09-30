"""
Pruebas: python manage.py test sitio

Renderizan TODAS las páginas definidas en contenido/ y comprueban que no haya
errores de plantilla, enlaces internos rotos ni imágenes inexistentes.
"""
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from sitio import contenido


class PaginasTest(SimpleTestCase):
    def test_todas_las_paginas_responden(self):
        for url in contenido.urls_paginas():
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, "<main id=\"contenido\">")

    def test_redirecciones(self):
        for antigua, nueva in contenido.cargar().redirecciones.items():
            with self.subTest(url=antigua):
                r = self.client.get(antigua)
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, f'url={nueva}')

    def test_404(self):
        self.assertEqual(self.client.get("/no-existe/").status_code, 404)

    def test_sitemap_y_robots(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "https://vrdaylatam.org/agenda/")
        self.assertNotContains(r, "/inicio-aries/")  # páginas ocultas fuera del sitemap
        self.assertEqual(self.client.get("/robots.txt").status_code, 200)

    def test_enlaces_internos_y_medios(self):
        """Todo href/src interno de cada página debe resolver."""
        paginas = set(contenido.urls_paginas()) | set(contenido.cargar().redirecciones)
        estaticos = Path(settings.BASE_DIR)
        rotos = []
        for url in contenido.urls_paginas():
            html = self.client.get(url).content.decode()
            for ref in re.findall(r'(?:href|src)="(/[^"#?]*)', html):
                if ref.startswith("/static/medios/"):
                    if not (Path(settings.MEDIOS_DIR) / ref.removeprefix("/static/medios/")).exists():
                        rotos.append((url, ref))
                elif ref.startswith("/static/"):
                    if not (estaticos / "static" / ref.removeprefix("/static/")).exists():
                        rotos.append((url, ref))
                elif ref not in paginas and ref not in ("/sitemap.xml",):
                    rotos.append((url, ref))
        self.assertEqual(rotos, [], f"Referencias rotas: {rotos}")

    @override_settings(SITIO_BASE="/vrday", STATIC_URL="/vrday/static/")
    def test_publicacion_en_subcarpeta(self):
        """GitHub Pages: todas las rutas internas deben llevar la subcarpeta."""
        sin_prefijo = []
        for url in contenido.urls_paginas():
            html = self.client.get(url).content.decode()
            for ref in re.findall(r'(?:href|src)="(/[^"]*)', html):
                if not ref.startswith(("/vrday/", "//")):
                    sin_prefijo.append((url, ref))
        self.assertEqual(sin_prefijo, [], f"Rutas sin subcarpeta: {sin_prefijo[:10]}")

    @override_settings(NO_INDEXAR=True)
    def test_vista_previa_no_indexable(self):
        self.assertContains(self.client.get("/"), '<meta name="robots" content="noindex">')
        self.assertContains(self.client.get("/robots.txt"), "Disallow: /")

    def test_menu_2026(self):
        r = self.client.get("/")
        for texto in ("Acerca de", "Ponentes", "Agenda", "Lugar", "Memorias", "Contacto"):
            self.assertContains(r, texto)
        self.assertContains(r, "Asamblea General RAIN Ecuador")   # resumen de agenda 2026
        self.assertContains(r, "Postulación de <strong>artículo</strong>")  # convocatoria vigente
        self.assertNotContains(r, "por confirmar")                  # aliados con publicar: false
