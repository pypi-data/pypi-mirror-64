# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rofi_menu', 'rofi_menu.contrib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rofi-menu',
    'version': '0.2.0',
    'description': 'Create rofi menus via python',
    'long_description': None,
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
