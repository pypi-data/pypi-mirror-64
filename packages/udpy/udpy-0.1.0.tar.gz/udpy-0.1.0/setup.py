# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udpy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'udpy',
    'version': '0.1.0',
    'description': 'Urban dictionary API wrapper for Python',
    'long_description': None,
    'author': 'prostomarkeloff',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
