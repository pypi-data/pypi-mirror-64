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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
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
