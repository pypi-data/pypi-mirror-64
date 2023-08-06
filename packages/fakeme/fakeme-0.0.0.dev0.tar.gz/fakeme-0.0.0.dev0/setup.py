# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fakeme', 'fakeme.cli']

package_data = \
{'': ['*'],
 'fakeme': ['examples/cli_usage/*',
            'examples/cli_usage/schemas/*',
            'examples/space_ship_parts/*']}

install_requires = \
['mimesis>=4.0,<5.0', 'pandas>=1.0,<2.0', 'ply>=3.11,<4.0']

entry_points = \
{'console_scripts': ['fakeme = fakeme.cli:cli']}

setup_kwargs = {
    'name': 'fakeme',
    'version': '0.0.0.dev0',
    'description': 'Relative Dataframes Generator: generate tables with data, that depend each other',
    'long_description': None,
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
