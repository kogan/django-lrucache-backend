DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3"},
}

SECRET_KEY = "notsosecret"

CACHES = {
    "lrumem": {
        "BACKEND": "lrucache_backend.LRUObjectCache",
        "OPTIONS": {"MAX_ENTRIES": 500, "CULL_FREQUENCY": 500},
    },
    "locmem": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "OPTIONS": {"MAX_ENTRIES": 500, "CULL_FREQUENCY": 500},
    },
}

CACHES["default"] = CACHES["lrumem"]
