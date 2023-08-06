# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_enhanced_settings']

package_data = \
{'': ['*']}

extras_require = \
{'cloud-secret-manager': ['google-cloud-secret-manager>=0.2.0,<0.3.0']}

setup_kwargs = {
    'name': 'django-enhanced-settings',
    'version': '0.2.1',
    'description': 'Allow for more complex and dynamic settings for Django',
    'long_description': "# django-enhanced-settings\n![Tests](https://github.com/OrangutanGaming/django-enhanced-settings/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings/branch/master/graph/badge.svg)](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings)\n[![PyPI](https://img.shields.io/pypi/v/django-enhanced-settings)](https://pypi.org/project/django-enhanced-settings/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-enhanced-settings)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-enhanced-settings)\n\nAllow for more complex and dynamic settings for Django.\n\n## Extras\n`cloud-secret-manager` - Adds support for Google Cloud Secret Manager\n\n## Example\n```py\nimport os\n\nfrom django_enhanced_settings import Settings\n\n\nBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n\nsettings = Settings(BASE_DIR)\n\n\ndef __dir__():\n    return settings.dir(globals())\n\n\ndef __getattr__(name):\n    return settings.getattr(name, globals())\n\n\n_DEBUG = settings.boolean_value('DJANGO_DEBUG', False)\n_ALLOWED_HOSTS = settings.list_value(\n    'DJANGO_ALLOWED_HOSTS',\n    ['localhost'] if _DEBUG.value else [],\n    split_char=';'\n)\n_SECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)\nINSTALLED_APPS = [...]\n```\n```py\nfrom django.conf import setings\n\nsettings.DEBUG  # By default returns False\n```\n\n## Rules\n1. You are not allowed to name a non `ConfigValue` using the naming scheme set for the `Settings` instance (`suffix_underscore`). For example, writing the following would raise a `ValueError` in the above example:\n```py\n_INSTALLED_APPS = [...]\n```\n2. You are not allowed to name a `ConfigValue` without using the naming scheme set for the `Settings` instance (`suffix_underscore`). For example, writing the following would raise a `ValueError` in the above example:\n```py\nSECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)\n```\n3. You are not allowed to define 2 variable names that result in the same accessible name. For example, writing the following would raise a `ValueError` in the above example:\n```py\n_SECRET_KEY = settings.string_value('DJANGO_SECRET_KEY', required=True)\nSECRET_KEY = 'SECRET_KEY'\n```\nIf you would like to customise these rules you can write your own `__dir__` and `__getattr__`.\n",
    'author': 'Nihaal Sangha',
    'author_email': '18350092+OrangutanGaming@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangutanGaming/django-enhanced-settings',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
