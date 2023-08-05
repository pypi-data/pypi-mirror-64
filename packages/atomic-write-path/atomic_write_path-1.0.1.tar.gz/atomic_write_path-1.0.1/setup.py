# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atomic_write_path']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.3,<2.0']

setup_kwargs = {
    'name': 'atomic-write-path',
    'version': '1.0.1',
    'description': 'Context manager for atomically writing data to a file path',
    'long_description': None,
    'author': 'Bao Wei',
    'author_email': 'baowei.ur521@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
