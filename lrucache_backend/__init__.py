from __future__ import absolute_import, unicode_literals

"""django-lrucache-backend - A smarter local memory cache backend for Django"""

from .backend import LRUObjectCache


__version__ = '0.2.0'
__author__ = 'Josh Smeaton <josh.smeaton@gmail.com>'
__all__ = ['LRUObjectCache']
