"""
python manage.py exportar [--borrador]

Genera el sitio estático completo en dist/ (listo para subir al hosting):
  1. valida el contenido (se detiene si hay errores),
  2. copia estáticos (collectstatic) y exporta todas las páginas con django-distill,
  3. oculta las marcas de "Contenido provisional" (salvo con --borrador).
"""
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.test.utils import override_settings


class Command(BaseCommand):
    help = "Valida el contenido y exporta el sitio estático a dist/."

    def add_arguments(self, parser):
        parser.add_argument("--borrador", action="store_true",
                            help="Muestra las marcas de contenido provisional (para revisión interna).")

    def handle(self, *args, **options):
        call_command("validar_contenido")
        # Desde cero: collectstatic no borra archivos que ya no existen (p. ej. PNG/JPG
        # reemplazados por WebP) y distill copiaría todo staticfiles/ al sitio publicado.
        for carpeta in (settings.STATIC_ROOT, settings.DISTILL_DIR):
            shutil.rmtree(carpeta, ignore_errors=True)
        with override_settings(MOSTRAR_PLACEHOLDERS=options["borrador"]):
            call_command("distill", "generate", collectstatic=True, force=True, quiet=True)
        # Con subcarpeta (p. ej. /vrday), distill copia los estáticos en dist/vrday/static,
        # pero el hosting sirve dist/ como /vrday/ → deben quedar en dist/static.
        if settings.SITIO_BASE:
            anidado = settings.DISTILL_DIR / settings.SITIO_BASE.strip("/")
            if (anidado / "static").is_dir():
                shutil.move(str(anidado / "static"), str(settings.DISTILL_DIR / "static"))
                shutil.rmtree(anidado, ignore_errors=True)
        html = sum(1 for _ in settings.DISTILL_DIR.rglob("*.html"))
        peso = sum(f.stat().st_size for f in settings.DISTILL_DIR.rglob("*") if f.is_file()) / 1e6
        base = f" · publicado bajo {settings.SITIO_BASE}/" if settings.SITIO_BASE else ""
        base += f" · estáticos en {settings.STATIC_URL}" if settings.STATIC_URL != f"{settings.SITIO_BASE}/static/" else ""
        self.stdout.write(self.style.SUCCESS(f"Sitio exportado en {settings.DISTILL_DIR} ({html} páginas HTML, {peso:.1f} MB){base}."))
