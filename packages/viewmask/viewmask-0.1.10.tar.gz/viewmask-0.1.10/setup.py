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
    'version': '0.1.10',
    'description': 'A Python package and CLI to view XML annotations and NumPy masks.',
    'long_description': 'viewmask\n========\nA Python package and CLI to view XML annotations and NumPy masks.\n\n|made-with-python|\n|made-with-sphinx-doc|\n|PyPI license|\n|PyPI version fury.io|\n|Documentation Status|\n\n.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/\n\n.. |made-with-sphinx-doc| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg\n  :target: https://www.sphinx-doc.org/\n\n.. |PyPI version fury.io| image:: https://badge.fury.io/py/viewmask.svg\n   :target: https://pypi.python.org/pypi/viewmask/\n\n.. |PyPI license| image:: https://img.shields.io/pypi/l/viewmask.svg\n  :target: https://pypi.python.org/pypi/viewmask/\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/viewmask/badge/?version=latest\n   :target: https://viewmask.readthedocs.io/?badge=latest\n',
    'author': 'sumanthratna',
    'author_email': 'sumanthratna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumanthratna/viewmask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
