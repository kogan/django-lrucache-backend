"""django-lrucache-backend - A smarter local memory cache backend for Django"""

from .backend import LRUObjectCache
from .backend_pure import LocMemObjectCache

__version__ = "4.0.0"
__author__ = "Josh Smeaton <josh.smeaton@gmail.com>"
__all__ = ["LRUObjectCache", "LocMemObjectCache"]
