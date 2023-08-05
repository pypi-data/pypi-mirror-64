# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ps_eor', 'ps_eor.tests']

package_data = \
{'': ['*']}

install_requires = \
['GPy>=1.9,<2.0',
 'astropy>=2,<3',
 'backports-functools_lru_cache>=1.5,<2.0',
 'configparser>=4.0,<5.0',
 'healpy>=1.12,<2.0',
 'matplotlib>=2,<3',
 'numpy>=1.10,<2.0',
 'pyfftw>=0.11.1,<0.12.0',
 'scikit-learn>=0.20,<0.21',
 'scipy>=1.2,<2.0',
 'tables>=3.2,<4.0']

setup_kwargs = {
    'name': 'ps-eor',
    'version': '0.6.0',
    'description': 'Foreground modeling/removal and Power Spectra generation',
    'long_description': None,
    'author': 'Florent Mertens',
    'author_email': 'flomertens@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
