"""Settings for testing environment deployed on Azure App Service
"""

import dj_database_url

from website.settings.base import *

ALLOWED_HOSTS = [
    'lkkpomia-testing.azurewebsites.net',
]

# WhiteNoise
MIDDLEWARE.extend(["whitenoise.middleware.WhiteNoiseMiddleware"])
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
