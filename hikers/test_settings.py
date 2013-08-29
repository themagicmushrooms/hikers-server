import warnings
warnings.simplefilter('always')

from .settings import *  # noqa

if not 'STATICFILES' in os.environ:
    STATICFILES_STORAGE = ('django.contrib.staticfiles'
                           '.storage.StaticFilesStorage')
EMAIL_HOST = 'dummy'
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

# Don't bother with PBKDF2 in tests. This saves a **lot** of time.
PASSWORD_HASHERS = [
    'tests.hashers.NotHashingHasher',
]

LOGGING['loggers']['ratelimitbackend']['level'] = 'ERROR'

INSTALLED_APPS += (
    'tests',
)

TESTS = True  # An easy way to determine whether we're running the tests or not

REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'
