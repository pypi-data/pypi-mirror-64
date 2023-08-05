# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fifo_test_poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fifo-test-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Zorgulle',
    'author_email': 'winy95battle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
