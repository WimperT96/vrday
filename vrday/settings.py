"""
Configuración del sitio VR Day LATAM.

Sitio 100 % informativo: sin base de datos, sin sesiones, sin admin.
El contenido se lee de contenido/*.yaml y las imágenes de medios/.
Se exporta a HTML estático con django-distill (ver README → "Exportar el sitio").
"""
import mimetypes
import os
from pathlib import Path

# El servidor de desarrollo de Windows no conoce woff2 (lo entrega como octet-stream).
mimetypes.add_type("font/woff2", ".woff2")

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
# Subcarpeta donde se publica el sitio (vacío = raíz del dominio).
# GitHub Pages publica en https://<usuario>.github.io/<repo>/ → VR_BASE_URL=/<repo>
SITIO_BASE = os.environ.get("VR_BASE_URL", "").strip().rstrip("/")
if SITIO_BASE and not SITIO_BASE.startswith("/"):
    SITIO_BASE = "/" + SITIO_BASE

# CSS, JS, fuentes e imágenes. Por defecto junto a las páginas (<base>/static/).
# VR_STATIC_URL los publica en otra ruta del mismo dominio, p. ej. dentro de un tema de
# WordPress (/wp-content/themes/vrday/static/) con las páginas en la raíz; la exportación
# deja los archivos en dist/ + esa ruta (ver docs/11-wordpress.md).
_STATIC_PROPIO = os.environ.get("VR_STATIC_URL", "").strip()
if _STATIC_PROPIO:
    STATIC_URL = "/" + _STATIC_PROPIO.strip("/") + "/"
else:
    STATIC_URL = f"{SITIO_BASE}/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("medios", BASE_DIR / "medios"),
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ── Contenido y exportación ─────────────────────────────────────────────────
CONTENIDO_DIR = BASE_DIR / "contenido"
MEDIOS_DIR = BASE_DIR / "medios"
DISTILL_DIR = BASE_DIR / "dist"

# Igual que el hosting estático (sin cabecera propia): los reproductores de YouTube
# necesitan recibir el dominio de origen; con "same-origin" (valor por defecto de Django)
# fallan en el servidor de desarrollo con "Video player configuration error".
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Vista previa pública (GitHub Pages): pide a los buscadores no indexar el sitio.
NO_INDEXAR = os.environ.get("VR_NOINDEX", "0") == "1"

# Marca visualmente el contenido provisional (placeholder: true) mientras se desarrolla.
MOSTRAR_PLACEHOLDERS = os.environ.get("VR_MOSTRAR_PLACEHOLDERS", "1" if DEBUG else "0") == "1"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"consola": {"class": "logging.StreamHandler"}},
    "loggers": {"sitio": {"handlers": ["consola"], "level": "WARNING"}},
}
