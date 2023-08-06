# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libdiff', 'libdiff.api', 'libdiff.bin', 'libdiff.core', 'libdiff.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libdiff',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lee Suho',
    'author_email': 'riemannulus@hitagi.moe',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
