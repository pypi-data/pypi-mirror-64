# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrclone']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyrclone',
    'version': '1.0.0',
    'description': 'pyRclone',
    'long_description': None,
    'author': 'Ryan C',
    'author_email': 'r.cross@lancaster.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
