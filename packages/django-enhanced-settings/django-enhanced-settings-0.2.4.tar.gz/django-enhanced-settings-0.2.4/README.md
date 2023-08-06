# django-enhanced-settings
![Tests](https://github.com/OrangutanGaming/django-enhanced-settings/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings/branch/master/graph/badge.svg)](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings)
[![PyPI](https://img.shields.io/pypi/v/django-enhanced-settings)](https://pypi.org/project/django-enhanced-settings/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-enhanced-settings)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-enhanced-settings)

Allow for more complex and dynamic settings for Django.

## Extras
`cloud-secret-manager` - Adds support for Google Cloud Secret Manager

## Example
```py
import os

from django_enhanced_settings import Settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings(BASE_DIR)


def __dir__():
    return settings.dir(globals())


def __getattr__(name):
    return settings.getattr(name, globals())


_DEBUG = settings.boolean_value('DJANGO_DEBUG', False)
_ALLOWED_HOSTS = settings.list_value(
    'DJANGO_ALLOWED_HOSTS',
    ['localhost'] if _DEBUG.value else [],
    split_char=';'
)
_SECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)
INSTALLED_APPS = [...]
```
```py
from django.conf import setings

settings.DEBUG  # By default returns False
```

## Rules
1. You are not allowed to name a non `ConfigValue` using the naming scheme set for the `Settings` instance (`suffix_underscore`). For example, writing the following would raise a `ValueError` in the above example:
```py
_INSTALLED_APPS = [...]
```
2. You are not allowed to name a `ConfigValue` without using the naming scheme set for the `Settings` instance (`suffix_underscore`). For example, writing the following would raise a `ValueError` in the above example:
```py
SECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)
```
3. You are not allowed to define 2 variable names that result in the same accessible name. For example, writing the following would raise a `ValueError` in the above example:
```py
_SECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)
SECRET_KEY = 'SECRET_KEY'
```
If you would like to customise these rules you can write your own `__dir__` and `__getattr__`.

## Cache values on first run
If you would like to cache all your static values at once, you can append `Settings.cache_static_values(...)` to the bottom of your settings file. For the example above, this would fetch `DEBUG`, `ALLOWED_HOSTS` and `SECRET_KEY`:
```py
settings.cache_static_values()
```
If you are not using `Settings.dir(...)` and `Settings.getattr(...)`, you may need to write your own function insead of using `Settings.cache_static_values(...)`.
