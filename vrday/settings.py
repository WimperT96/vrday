"""
Configuración del sitio VR Day LATAM.

Sitio 100 % informativo: sin base de datos, sin sesiones, sin admin.
El contenido se lee de contenido/*.yaml y las imágenes de medios/.
Se exporta a HTML estático con django-distill (ver README → "Exportar el sitio").
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Sin sesiones ni formularios: la clave solo es necesaria para que Django arranque.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "solo-desarrollo-local-sitio-estatico")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver"] + [
    h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h
]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_distill",
    "sitio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "vrday.urls"
WSGI_APPLICATION = "vrday.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "sitio.context_processors.sitio",
            ],
            "builtins": [
                "django.templatetags.static",
                "sitio.templatetags.vr",
            ],
        },
    }
]

DATABASES = {}

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = False
USE_TZ = True

# ── Archivos estáticos ───────────────────────────────────────────────────────
# medios/ se publica bajo /static/medios/ para que el contenido use rutas cortas
# (p. ej. "ponentes/2023/aura-forero.png").
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("medios", BASE_DIR / "medios"),
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ── Contenido y exportación ─────────────────────────────────────────────────
CONTENIDO_DIR = BASE_DIR / "contenido"
MEDIOS_DIR = BASE_DIR / "medios"
DISTILL_DIR = BASE_DIR / "dist"

# Marca visualmente el contenido provisional (placeholder: true) mientras se desarrolla.
MOSTRAR_PLACEHOLDERS = os.environ.get("VR_MOSTRAR_PLACEHOLDERS", "1" if DEBUG else "0") == "1"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"consola": {"class": "logging.StreamHandler"}},
    "loggers": {"sitio": {"handlers": ["consola"], "level": "WARNING"}},
}
