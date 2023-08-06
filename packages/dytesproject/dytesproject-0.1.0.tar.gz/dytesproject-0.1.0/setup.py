# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dytesproject']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dytesproject',
    'version': '0.1.0',
    'description': 'Dyens test project',
    'long_description': None,
    'author': 'Kapustin Alexander',
    'author_email': 'akapustin@ambrahealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
