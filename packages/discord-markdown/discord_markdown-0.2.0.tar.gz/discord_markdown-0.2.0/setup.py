# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_markdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discord-markdown',
    'version': '0.2.0',
    'description': 'Convert discord messages to HTML',
    'long_description': None,
    'author': 'BitJockey',
    'author_email': 'bitjockey@jackpoint.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
