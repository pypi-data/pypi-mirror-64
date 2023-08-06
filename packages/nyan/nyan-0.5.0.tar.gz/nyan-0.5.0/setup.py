# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nyan']

package_data = \
{'': ['*']}

install_requires = \
['pefile>=2019.4.18,<2020.0.0',
 'pygame>=1.9.6,<2.0.0',
 'pyinstaller>=3.6,<4.0',
 'pypiwin32>=223,<224',
 'pytest>=5.2,<6.0',
 'pywin32-ctypes>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['nyan-packager = nyan_packager:run']}

setup_kwargs = {
    'name': 'nyan',
    'version': '0.5.0',
    'description': 'The easiest way to transition from Scratch to Python',
    'long_description': None,
    'author': 'ducaale',
    'author_email': 'sharaf.13@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
