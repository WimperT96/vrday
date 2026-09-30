"""
python manage.py validar_contenido

Ejecuta referencias/herramientas/validar_contenido.py (imágenes, enlaces internos,
PENDIENTES) y además comprueba que cada tipo de sección tenga su plantilla.
"""
import runpy
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sitio import contenido


class Command(BaseCommand):
    help = "Valida contenido/*.yaml: medios, enlaces internos, plantillas y pendientes."

    def handle(self, *args, **options):
        errores = []
        componentes = settings.BASE_DIR / "templates" / "components"
        for url, pagina in contenido.cargar().paginas.items():
            for s in pagina.get("secciones", []):
                tipo = s.get("tipo")
                if not tipo:
                    errores.append(f"{pagina['_archivo']}: sección sin 'tipo'")
                elif not (componentes / f"{tipo}.html").exists():
                    errores.append(f"{pagina['_archivo']}: no existe templates/components/{tipo}.html")
        for e in errores:
            self.stderr.write(f"  x {e}")

        script = settings.BASE_DIR / "referencias" / "herramientas" / "validar_contenido.py"
        try:
            runpy.run_path(str(script), run_name="__main__")
        except SystemExit as salida:
            if salida.code or errores:
                raise CommandError("La validación encontró errores.")
        sys.stdout.flush()
