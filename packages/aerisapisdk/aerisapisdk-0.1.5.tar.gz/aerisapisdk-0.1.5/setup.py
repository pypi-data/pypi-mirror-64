# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerisapisdk']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pathlib>=1.0.1,<2.0.0', 'requests>=2.22,<3.0']

extras_require = \
{':sys_platform == "win32"': ['pywin32>=227,<228']}

entry_points = \
{'console_scripts': ['aeriscli = aerisapisdk.cli:main']}

setup_kwargs = {
    'name': 'aerisapisdk',
    'version': '0.1.5',
    'description': 'Provides both an SDK and a CLI for the Aeris Connectivity APIs.',
    'long_description': '# Getting Started\n\n```\n$ pip install aerisapisdk\n$ aeriscli --help\nUsage: aeriscli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -v, --verbose             Verbose output\n  -cfg, --config-file TEXT  Path to config file.\n  --help                    Show this message and exit.\n\nCommands:\n  aeradmin    AerAdmin API Services\n  aerframe    AerFrame API Services\n  aertraffic  AerTraffic API Services\n  config      Set up the configuration for using this tool\n  ping        Simple ping of the api endpoints\n```\n\n# More Information\n\nCheck out the [wiki](https://github.com/aeristhings/aeris-apisdk-py/wiki) for more information.\n',
    'author': 'Aeris Communications',
    'author_email': 'aeris-api-publisher@aeris.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aeristhings/aeris-apisdk-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
