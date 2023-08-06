# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dict_typer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['dict-typer = dict_typer:cli']}

setup_kwargs = {
    'name': 'dict-typer',
    'version': '0.1.0',
    'description': 'A simple library to take data and turn it into python typing definitions.',
    'long_description': None,
    'author': 'Axel',
    'author_email': 'dict.typer@absalon.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
