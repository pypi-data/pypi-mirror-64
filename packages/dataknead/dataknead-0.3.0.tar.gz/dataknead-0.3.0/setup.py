# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataknead', 'dataknead.loaders']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24.2,<0.25.0',
 'pyyaml>=5.1,<6.0',
 'xlrd>=1.2,<2.0',
 'xlwt>=1.3,<2.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['knead = dataknead.console:run']}

setup_kwargs = {
    'name': 'dataknead',
    'version': '0.3.0',
    'description': 'A fluid Python library and command line utility for processing and converting between data formats like JSON and CSV.',
    'long_description': None,
    'author': 'Hay Kranen',
    'author_email': 'huskyr@gmail.com',
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
