# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['bagitfs']
install_requires = \
['bagit==1.7.0', 'fs==2.2.1']

setup_kwargs = {
    'name': 'bagitfs',
    'version': '0.1.0',
    'description': 'Bagit package',
    'long_description': None,
    'author': 'Radim Spigel',
    'author_email': 'spigel@cesnet.cz',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
