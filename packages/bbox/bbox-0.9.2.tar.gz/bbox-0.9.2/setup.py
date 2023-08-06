# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbox']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.2,<2.0.0', 'pyquaternion>=0.9.5,<0.10.0']

setup_kwargs = {
    'name': 'bbox',
    'version': '0.9.2',
    'description': 'Python library for 2D/3D bounding boxes',
    'long_description': None,
    'author': 'Varun Agrawal',
    'author_email': 'varagrawal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
