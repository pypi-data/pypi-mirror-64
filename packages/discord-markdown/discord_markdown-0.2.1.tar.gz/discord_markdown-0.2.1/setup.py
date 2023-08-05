# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_markdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discord-markdown',
    'version': '0.2.1',
    'description': 'Convert discord messages to HTML',
    'long_description': '# Discord Markdown\n\nI needed to parse some Discord chat logs for something, and found that the Markdown implementation isn\'t compliant with Common Markdown as Discord uses a simplified version.\n\nThis is very early stage and probably won\'t be ready for use for awhile.\n\n```python\nfrom discord_markdown.discord_markdown import convert_to_html\n\nconvert_to_html("_This_ **is** an __example__.\\nThis should be a different paragraph.")\n```\n',
    'author': 'BitJockey',
    'author_email': 'bitjockey@jackpoint.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bitjockey42/discord-markdown',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
