import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["SniperHQ.pythonanywhere.com", "localhost", "127.0.0.1"]

# Media / Cloudinary
USE_CLOUDINARY = not DEBUG and all([
    os.environ.get("CLOUDINARY_CLOUD_NAME"),
    os.environ.get("CLOUDINARY_API_KEY"),
    os.environ.get("CLOUDINARY_API_SECRET"),
])

if USE_CLOUDINARY:
    import cloudinary
    cloudinary.config(
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
        secure=True,
    )
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = "/media/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database (SQLite is fine for small portfolio)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
