# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

from backend.constants import (
    PG_HOST,
    PG_DATABASE,
    PG_USER,
    PG_PASSWORD,
    PG_PORT,
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": PG_DATABASE,
        "USER": PG_USER,
        "PASSWORD": PG_PASSWORD,
        "HOST": PG_HOST,
        "PORT": PG_PORT,
    }
}
