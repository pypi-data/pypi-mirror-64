# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_schema_checker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'json-schema-checker',
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
