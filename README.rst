django-lrucache-backend
=======================

.. image:: https://img.shields.io/pypi/v/django-lrucache-backend.svg
    :target: https://pypi.python.org/pypi/django-lrucache-backend
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/kogan/django-lrucache-backend.png
   :target: https://travis-ci.org/kogan/django-lrucache-backend
   :alt: Latest Travis CI build status

A smarter local memory cache backend for Django.

Installation
------------

.. code-block:: bash

     pip install django-lrucache-backend

Requirements
^^^^^^^^^^^^

* [lru-dict](https://pypi.python.org/pypi/lru-dict/)

`lru-dict` is implemented in C and is unlikely to work with non-CPython
implementations. There *are* compatible pure python libraries. If you need this
ability, please open an Issue!

Usage
-----

Configure your `CACHES` Django setting appropriately:

.. code-block:: python

    CACHES = {
        'local': {
            'BACKEND': 'lrucache_backend.LRUObjectCache',
            'TIMEOUT': 600,
            'OPTIONS': {
                'MAX_ENTRIES': 50
            },
            'NAME': 'optional-name'
        }
    }

And then use the cache as you would any other:

.. code-block:: python

    >>> from django.core.cache import caches

    >>> local = caches['local']
    >>> local.set('key', 123)
    >>> local.get('key')
    ... 123

If you're going to use this cache backend, then it's highly recommended to use
it as a non-default cache. That is, do not configure this cache under the
`default` name.

Local memory caches compete for memory with your application so it's in your
best interests to use it as sparingly and deliberately as possible.

Compatibility
-------------

Django 1.8 - Django master. All Python versions supported by compatible Django
versions.

Licence
-------

MIT

Authors
-------

`django-lrucache-backend` was written by `Josh Smeaton <josh.smeaton@gmail.com>`_.
