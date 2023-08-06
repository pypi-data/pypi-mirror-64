# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sidebar_menu']

package_data = \
{'': ['*'], 'sidebar_menu': ['templates/sidebar_menu/*']}

install_requires = \
['django>=2']

setup_kwargs = {
    'name': 'django-sidebar-menu',
    'version': '0.1.0',
    'description': 'Create sidebar menu easily',
    'long_description': '# django-sidebar-menu\n\n[![Coverage Status](https://coveralls.io/repos/github/CleitonDeLima/django-sidebar-menu/badge.svg?branch=master)](https://coveralls.io/github/CleitonDeLima/django-sidebar-menu?branch=master)\n',
    'author': 'Cleiton Lima',
    'author_email': 'cleiton.limapin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CleitonDeLima/django-easy-tenants',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
