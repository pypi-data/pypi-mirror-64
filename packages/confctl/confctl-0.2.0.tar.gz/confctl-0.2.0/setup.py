# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confctl']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'jinja2>=2.11.1,<3.0.0']

entry_points = \
{'console_scripts': ['poetry = confctl.cli:main']}

setup_kwargs = {
    'name': 'confctl',
    'version': '0.2.0',
    'description': 'Simple configuration management',
    'long_description': '# confctl\n\nHelps to organize you configs and how they generated, installed.\n\n\n## Installation\n\n```sh\n$ pip install confctl\n```\n\n\n## Getting started\n\nTBD',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/confctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
