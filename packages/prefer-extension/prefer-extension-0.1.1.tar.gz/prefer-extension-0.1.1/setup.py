# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefer_extension']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'funcy>=1.14,<2.0']

entry_points = \
{'console_scripts': ['prefer-extension = prefer_extension.cli:process']}

setup_kwargs = {
    'name': 'prefer-extension',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Brian Sunter',
    'author_email': 'brian@briansunter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
