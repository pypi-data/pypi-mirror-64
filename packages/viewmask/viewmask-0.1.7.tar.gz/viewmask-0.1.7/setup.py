# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viewmask']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.0.0,<8.0.0',
 'click>=7.1.1,<8.0.0',
 'napari>=0.2.12,<0.3.0',
 'numpy>=1.18.1,<2.0.0',
 'opencv-python-headless>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['viewmask = viewmask.cli:cli']}

setup_kwargs = {
    'name': 'viewmask',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'sumanthratna',
    'author_email': 'sumanthratna@gmail.com',
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
