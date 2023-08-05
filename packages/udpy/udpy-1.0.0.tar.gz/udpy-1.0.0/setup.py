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
    'version': '1.0.0',
    'description': 'Urban dictionary API wrapper for Python',
    'long_description': "# urbandictionary-py\nSimple Python wrapper for Urban Dictionary API.\n\n## Installation\n\nWith PyPI:\n```\npip install udpy\n```\n\n## Usage\n\n### UrbanDefinition\n\nThis module defines **UrbanDefinition**, an object to represent each Urban Dictionary definition.\n**UrbanDefinition** has the following accessible attributes:\n* **word**: the word being defined,\n* **definition**: the word's definition,\n* **example**: usage example,\n* **upvotes**: number of upvotes on Urban Dictionary,\n* **downvotes**: number of downvotes on Urban Dictionary\n\n### Examples\n\nCreate client:\n```python\nfrom udpy import UrbanClient\n\nclient = UrbanClient()\n```\n\nLookup by word:\n```python\ndefs = client.get_definition('netflix and chill')\n\n>\t[List of UrbanDef objects]\n```\n\nLookup random words:\n```python\nrand = client.get_random_definition()\n\n>\t[List of UrbanDef objects]\n```\n\nRead definitions:\n```python\nfor d in defs:\n\tprint(d.definition)\n\n>\tIt means that you are going to go over ...\n>\tcode for two people going to each others ...\n> \t<other Netflix and Chill definitions> ...\n```\n\nUrbanDefinition string representation:\n```python\nfor d in defs:\n\tprint(d)\n\n>\tNetflix and Chill: It means that you are going to go over to your par... (21776, 7750)\n>\tnetflix and chill: code for two people going to each others houses an... (8056, 2622)\n>\t<word>: <definition trimmed to 50 characters> (<upvotes>, <downvotes>)\n```\n\n",
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
