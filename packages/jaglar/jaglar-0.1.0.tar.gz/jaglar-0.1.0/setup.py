# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaglar']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'pandas>=1.0.3,<2.0.0',
 'pydash>=4.7.6,<5.0.0',
 'xlrd>=1.2.0,<2.0.0',
 'xmljson>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['jaglar = jaglar.cli:main']}

setup_kwargs = {
    'name': 'jaglar',
    'version': '0.1.0',
    'description': 'Tool for project management backed by taskjuggler.',
    'long_description': None,
    'author': 'Abhinav Tushar',
    'author_email': 'abhinav@lepisma.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vernacular-ai/jaglar/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
