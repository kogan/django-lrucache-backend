DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'notsosecret'

CACHES = {
    'default': {
        'BACKEND': 'lrucache_backend.LRUObjectCache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
        'NAME': 'testingcache'
    },
    'lrumem': {
        'BACKEND': 'lrucache_backend.LRUObjectCache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
        'NAME': 'testingcache'
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 10,
        }
    }
}
