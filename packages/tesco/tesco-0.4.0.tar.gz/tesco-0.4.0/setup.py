# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tesco']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tesco',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Tesco\n\n A Python wrapper for the Tesco API\n\n Install: `$ pip install tesco`',
    'author': 'Miles Budden',
    'author_email': 'miles@budden.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pbexe/tesco',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
