from decouple import config

PG_HOST = config("PG_HOST", cast=str)
PG_DATABASE = config("PG_DATABASE", cast=str)
PG_USER = config("PG_USER", cast=str)
PG_PASSWORD = config("PG_PASSWORD", cast=str)
PG_PORT = config("PG_PORT", cast=int)

REDIS_BROKER_URL = config("REDIS_BROKER_URL", cast=str)
REDIS_BACKEND_URL = config("REDIS_BACKEND_URL", cast=str)

SECRET_KEY = config("SECRET_KEY", cast=str)

DEBUG = config("DEBUG", cast=bool)