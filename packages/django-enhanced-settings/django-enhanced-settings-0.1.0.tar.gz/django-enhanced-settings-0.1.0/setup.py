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
    'version': '0.1.0',
    'description': 'Allow for more complex and dynamic settings for Django',
    'long_description': None,
    'author': 'Nihaal Sangha',
    'author_email': '18350092+OrangutanGaming@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
