# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_liquibase']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-liquibase',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mateo Upegui Borja',
    'author_email': 'upeguiborja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
