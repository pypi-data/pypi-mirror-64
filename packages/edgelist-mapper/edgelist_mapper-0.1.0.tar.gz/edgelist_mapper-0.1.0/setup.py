# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edgelist_mapper', 'edgelist_mapper.bin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'edgelist-mapper',
    'version': '0.1.0',
    'description': 'Convert an edgelist file into a more compact format',
    'long_description': None,
    'author': 'Simone Primarosa',
    'author_email': 'simonepri@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
