DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'notsosecret'

CACHES = {
    'default': {
        'BACKEND': 'lrucache_backend.LRUObjectCache',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 50
        },
        'NAME': 'testingcache'
    },
}
