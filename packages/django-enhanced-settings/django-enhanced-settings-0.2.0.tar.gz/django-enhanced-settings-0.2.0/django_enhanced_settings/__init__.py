from importlib.metadata import version as _version

from .settings import Settings

__all__ = ['Settings']
__version__ = _version('django-enhanced-settings')
