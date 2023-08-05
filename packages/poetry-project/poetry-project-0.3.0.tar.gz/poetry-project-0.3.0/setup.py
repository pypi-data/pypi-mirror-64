# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_project']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.5.0,<2.0.0',
 'importlib-resources>=1.4.0,<2.0.0',
 'tomlkit>=0.5.11,<0.6.0']

setup_kwargs = {
    'name': 'poetry-project',
    'version': '0.3.0',
    'description': 'Read poetry project information such as name, version and description.',
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
