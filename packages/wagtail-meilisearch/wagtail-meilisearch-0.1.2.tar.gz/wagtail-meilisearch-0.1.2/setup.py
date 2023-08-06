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
    'version': '0.1.2',
    'description': 'A MeiliSearch backend for Wagatil',
    'long_description': "# Wagtail MeiliSearch\n\nThis is a (beta) Wagtail search backend for the [MeiliSearch](https://github.com/meilisearch/MeiliSearch) search engine.\n\n\n## Installation\n\n`poetry add wagtail_meilisearch` or `pip install wagtail_meilisearch`\n\n## Configuration\n\nSee the [MeiliSearch docs](https://docs.meilisearch.com/guides/advanced_guides/installation.html#environment-variables-and-flags) for info on the values you want to add here.\n\n```\nWAGTAILSEARCH_BACKENDS = {\n    'default': {\n        'BACKEND': 'wagtail_meilisearch.backend',\n        'HOST': os.environ.get('MEILISEARCH_HOST', 'http://127.0.0.1'),\n        'PORT': os.environ.get('MEILISEARCH_PORT', '7700'),\n        'MASTER_KEY': os.environ.get('MEILI_MASTER_KEY', '')\n    },\n}\n```\n\n## Stop Words\n\nStop words are words for which we don't want to place significance on their frequency. For instance, the search query `tom and jerry` would return far less relevant results if the word `and` was given the same importance as `tom` and `jerry`. There's a fairly sane list of English language stop words supplied, but you can also supply your own. This is particularly useful if you have a lot of content in any other language.\n\n```\nMY_STOP_WORDS = ['a', 'list', 'of', 'words']\n\nWAGTAILSEARCH_BACKENDS = {\n    'default': {\n        'BACKEND': 'wagtail_meilisearch.backend',\n        [...]\n        'STOP_WORDS': MY_STOP_WORDS\n    },\n}\n```\n\nOr alternatively, you can extend the built in list.\n\n```\nfrom wagtail_meilisearch.settings import STOP_WORDS\n\nMY_STOP_WORDS = STOP_WORDS + WELSH_STOP_WORDS + FRENCH_STOP_WORDS\n\nWAGTAILSEARCH_BACKENDS = {\n    'default': {\n        'BACKEND': 'wagtail_meilisearch.backend',\n        [...]\n        'STOP_WORDS': MY_STOP_WORDS\n    },\n}\n```\n\n\n## Contributing\n\nIf you want to help with the development I'd be more than happy. The vast majority of the heavy lifting is done by MeiliSearch itself, but there is a TODO list...\n\n\n### TODO\n\n* Faceting\n* Implement boosting in the sort algorithm\n* Write tests\n* Performance improvements - particularly in the autocomplete query compiler which for some reason seems slower than the regular one.\n* ~~Implement stop words~~\n* ~~Search results~~\n* ~~Add support for the autocomplete api~~\n* ~~Ensure we're getting results by relevance~~\n\n### Thanks\n\nThank you to the devs of [Wagtail-Whoosh](https://github.com/wagtail/wagtail-whoosh). Reading the code over there was the only way I could work out how Wagtail Search backends are supposed to work.\n",
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
