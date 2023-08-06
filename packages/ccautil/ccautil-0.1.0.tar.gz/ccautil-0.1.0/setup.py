# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccautil']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ccautil',
    'version': '0.1.0',
    'description': 'a set of utilities',
    'long_description': '',
    'author': 'Chris Allison',
    'author_email': 'chris.charles.allison+ccautil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/ccautil',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
