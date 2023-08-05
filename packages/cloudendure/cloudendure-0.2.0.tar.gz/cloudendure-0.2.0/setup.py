# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudendure',
 'cloudendure.cloudendure_api',
 'cloudendure.cloudendure_api.api',
 'cloudendure.cloudendure_api.models',
 'cloudendure.cloudendure_api.test',
 'cloudendure.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.4,<2.0.0',
 'certifi>=2019.11.28,<2020.0.0',
 'cookiecutter>=1.7.0,<2.0.0',
 'fire>=0.2.1,<0.3.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'setuptools>=45.2.0,<46.0.0',
 'six>=1.14.0,<2.0.0',
 'urllib3>=1.25.8,<2.0.0']

entry_points = \
{'console_scripts': ['ce = cloudendure.cloudendure:main',
                     'cloudendure = cloudendure.cloudendure:main']}

setup_kwargs = {
    'name': 'cloudendure',
    'version': '0.2.0',
    'description': 'Python wrapper and CLI for CloudEndure',
    'long_description': None,
    'author': 'Mark Beacom',
    'author_email': 'mark@markbeacom.com',
    'maintainer': 'Evan Lucchesi',
    'maintainer_email': 'evan@2ndwatch.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
