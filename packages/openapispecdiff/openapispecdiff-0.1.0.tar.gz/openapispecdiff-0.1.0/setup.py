# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapispecdiff']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['openapidiff = OpenApiSpecDiff.OpenApiSpecDiff:main']}

setup_kwargs = {
    'name': 'openapispecdiff',
    'version': '0.1.0',
    'description': 'Difference between two OpenAPISpec files',
    'long_description': None,
    'author': 'Bala',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
