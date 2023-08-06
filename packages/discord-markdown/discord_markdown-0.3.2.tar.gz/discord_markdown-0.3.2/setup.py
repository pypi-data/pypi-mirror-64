# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_markdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discord-markdown',
    'version': '0.3.2',
    'description': 'Convert discord messages to HTML',
    'long_description': '# Discord Markdown\n\nI needed to render some Discord chat logs as HTML, and found that the Markdown implementation in Discord isn\'t quite compliant with Common Markdown as Discord uses a simplified version. \n\nSo I wrote this library that allows you to convert a discord message written in the Markdown formatting syntax specified [here](https://support.discordapp.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-) to html.\n\n\n## Installation\n\nYou can install the library from `pypi`:\n\n```sh\npip install discord-markdown\n```\n\n## Usage\n\n```python\nfrom discord_markdown.discord_markdown import convert_to_html\n\ntext = "_This_ **is** an __example__.\\nThis should be a different paragraph."\nhtml = convert_to_html(text)\n\nassert html == \'<p><i>This</i> <b>is</b> an <u>example</u>.</p><p>This should be a different paragraph.</p>\'\n```\n',
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
