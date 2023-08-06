# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confctl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'confctl',
    'version': '0.1.0',
    'description': 'Simple configuration management',
    'long_description': '# confctl\n\nHelps to organize you configs and how they generated, installed.\n\n\n## Installation\n\n```sh\n$ pip install confctl\n```\n\n\n## Getting started\n\nTBD',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/confctl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
