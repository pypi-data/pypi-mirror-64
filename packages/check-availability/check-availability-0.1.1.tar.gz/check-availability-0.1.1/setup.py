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
    'version': '0.1.1',
    'description': '',
    'long_description': 'check-availability\n====\n\n\n\n## Installation\n\n```sh-session\n$ pip install check_availability\n```\n\n## Usage\n\n```sh-session\n$ check-availability <service> <name> [options]\n```\n\n## Example\n\n```sh-session\n$ check-availability pypi check_availability\nGET https://pypi.org/project/check_availability\nGot status code 200\nThe name check_availability is not available on pypi\n```\n\n## Options\n\n| Shorthand | Option | Description | Default value\n|-----------|-------------|-------------|--------------\n| -h | --help | Show the help. | N/A |\n| -v | --verbose=LEVEL | Set verbosity. 0 for quiet, 4 for debug. | 0 |\n\n## Status codes\n\n| Code | Meaning\n|------|--------\n| 0 | The name is available\n| 1 | An error occured\n| 2 | The name is not available\n',
    'author': 'ewen-lbh',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/check-availability',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
