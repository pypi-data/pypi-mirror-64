# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_project']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.11,<0.6.0']

setup_kwargs = {
    'name': 'poetry-project',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Stier',
    'author_email': 'mail@julian-stier.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
