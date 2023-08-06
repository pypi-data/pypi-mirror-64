# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subgrab', 'subgrab.providers', 'subgrab.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.5.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'typing>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['subgrab = subgrab.cli:main']}

setup_kwargs = {
    'name': 'subgrab',
    'version': '1.0.1',
    'description': 'Automate subtitles fetching',
    'long_description': None,
    'author': 'Rafay Ghafoor',
    'author_email': 'rafayghafoor@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
