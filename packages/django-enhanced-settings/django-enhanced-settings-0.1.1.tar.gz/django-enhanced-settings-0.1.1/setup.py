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
    'version': '0.1.1',
    'description': 'Allow for more complex and dynamic settings for Django',
    'long_description': '# django-enhanced-settings\n![Tests](https://github.com/OrangutanGaming/django-enhanced-settings/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings/branch/master/graph/badge.svg)](https://codecov.io/gh/OrangutanGaming/django-enhanced-settings)\n[![PyPI](https://img.shields.io/pypi/v/django-enhanced-settings)](https://pypi.org/project/django-enhanced-settings/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-enhanced-settings)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-enhanced-settings)\n\nAllow for more complex and dynamic settings for Django\n',
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
