# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fits_schema']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=3.0', 'numpy>=1.16,<2.0']

extras_require = \
{'travis': ['codecov>=2.0.22,<3.0.0']}

setup_kwargs = {
    'name': 'fits-schema',
    'version': '0.1.0.post1',
    'description': '',
    'long_description': '# fits_schema [![Build Status](https://travis-ci.com/open-gamma-ray-astro/fits_schema.svg?branch=master)](https://travis-ci.com/open-gamma-ray-astro/fits_schema) [![codecov](https://codecov.io/gh/open-gamma-ray-astro/fits_schema/branch/master/graph/badge.svg)](https://codecov.io/gh/open-gamma-ray-astro/fits_schema)\n\n\n\nA python package to define and validate schemata for FITS files.\n',
    'author': 'Maximilian Nöthe',
    'author_email': 'maximilian.noethe@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
