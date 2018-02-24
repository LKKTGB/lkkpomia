import dj_database_url

from website.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    'lkkpomia.tgb.org.tw',
    'lkk-website-production.herokuapp.com',
]

# WhiteNoise
MIDDLEWARE.extend([
    'whitenoise.middleware.WhiteNoiseMiddleware',
])
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
