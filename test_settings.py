DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3"},
}

SECRET_KEY = "notsosecret"

CACHES = {
    "default": {
        "BACKEND": "lrucache_backend.LRUObjectCache",
        "TIMEOUT": 600,
        "OPTIONS": {"MAX_ENTRIES": 50, "CULL_FREQUENCY": 50},
        "NAME": "testingcache",
    },
    "locmem": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "OPTIONS": {"MAX_ENTRIES": 50, "CULL_FREQUENCY": 50},
    },
}
