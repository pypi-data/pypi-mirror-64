# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['check_availability']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'pastel>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['check-availability = check_availability.cli:run']}

setup_kwargs = {
    'name': 'check-availability',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ewen-lbh',
    'author_email': 'ewen.lebihan7@gmail.com',
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
