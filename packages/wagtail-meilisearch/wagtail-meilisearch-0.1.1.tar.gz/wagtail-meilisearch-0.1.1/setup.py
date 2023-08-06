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
    'version': '0.1.1',
    'description': 'A MeiliSearch backend for Wagatil',
    'long_description': "# Wagtail MeiliSearch\n\nThis is a (beta) Wagtail search backend for the [https://github.com/meilisearch/MeiliSearch](MeiliSearch) search engine.\n\n\n## Installation\n\n`poetry add wagtail_meilisearch` or `pip install wagtail_meilisearch`\n\n## Configuration\n\nSee the [https://docs.meilisearch.com/guides/advanced_guides/installation.html#environment-variables-and-flags](MeiliSearch docs) for info on the values you want to add here.\n\n```\nWAGTAILSEARCH_BACKENDS = {\n    'default': {\n        'BACKEND': 'wagtail_meilisearch.backend',\n        'HOST': os.environ.get('MEILISEARCH_HOST', 'http://127.0.0.1'),\n        'PORT': os.environ.get('MEILISEARCH_PORT', '7700'),\n        'MASTER_KEY': os.environ.get('MEILI_MASTER_KEY', '')\n    },\n}\n```\n\n## Contributing\n\nIf you want to help with the development I'd be more than happy. The vast majority of the heavy lifting is done by MeiliSearch itself, but there is a TODO list...\n\n\n### TODO\n\n* Faceting\n* Implement boosting in the sort algorithm\n* ~~Search results~~\n* ~~Add support for the autocomplete api~~\n* ~~Ensure we're getting results by relevance~~\n* Write tests\n* Performance improvements - particularly in the autocomplete query compiler which for some reason seems slower than the regular one.\n\n### Thanks\n\nThank you to the devs of [https://github.com/wagtail/wagtail-whoosh](Wagtail-Whoosh). Reading the code over there was the only way I could work out how Wagtail Search backends are supposed to work.\n",
    'author': 'Hactar',
    'author_email': 'systems@hactar.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hactar-is/wagtail-meilisearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
