# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib_conda_project']

package_data = \
{'': ['*']}

install_requires = \
['xonsh']

setup_kwargs = {
    'name': 'xontrib-conda-project',
    'version': '0.1.0',
    'description': 'Automatically activate conda environments when switching projects',
    'long_description': None,
    'author': 'Dominic Ward',
    'author_email': 'dom@deeuu.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
