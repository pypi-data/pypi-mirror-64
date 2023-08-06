# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_loop']

package_data = \
{'': ['*']}

install_requires = \
['cli-ui>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['looper = py_loop.main:main']}

setup_kwargs = {
    'name': 'py-loop',
    'version': '0.4.0',
    'description': 'Run commands until it fails',
    'long_description': None,
    'author': 'jerem',
    'author_email': 'jeremy.tellaa@tanker.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
