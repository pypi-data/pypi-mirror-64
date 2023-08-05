# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['drf_yasg_examples']
install_requires = \
['drf-yasg>=1.17.1,<2.0.0']

setup_kwargs = {
    'name': 'drf-yasg-examples',
    'version': '0.1.0',
    'description': 'Inspector for add example in drf-yasg docs',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
