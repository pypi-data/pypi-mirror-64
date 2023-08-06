# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_meilisearch']

package_data = \
{'': ['*']}

install_requires = \
['meilisearch>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'wagtail-meilisearch',
    'version': '0.1.0',
    'description': 'A MeiliSearch backend for Wagatil',
    'long_description': None,
    'author': 'Hactar',
    'author_email': 'systems@hactar.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
