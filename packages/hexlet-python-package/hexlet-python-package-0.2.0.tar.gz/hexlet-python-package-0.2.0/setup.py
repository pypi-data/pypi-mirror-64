# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hexlet_python_package', 'hexlet_python_package.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hexlet-python-package = '
                     'hexlet_python_package.scripts.hexlet_python_package:main']}

setup_kwargs = {
    'name': 'hexlet-python-package',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'skip',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
