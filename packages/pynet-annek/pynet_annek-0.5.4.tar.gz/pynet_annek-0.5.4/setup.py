# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynet_annek']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'netmiko>=2.4,<3.0', 'termcolor>=1.1,<2.0']

entry_points = \
{'console_scripts': ['pynet = pynet_annek.cli:main']}

setup_kwargs = {
    'name': 'pynet-annek',
    'version': '0.5.4',
    'description': 'A cli for managing network switches',
    'long_description': '# pynet #\nA cli tool for interacting with network switches\n\n## Synopsis ##\n\n> pynet is a cli tool for running adhoc commands and getting version information and configurations\n> from network devices. It stores devices in a sqlite database. It can then query those devices and\n> store some basic information about devices in the database.\n>\n> pynet supports csv import of devices to the database. If you have a bunch of network devices that\n> are configured via ssh and you need to retrieve version information from all of those devices, pynet\n> can help you accomplish that task.\n>\n> pynet is a basic tool created to perform some necessary tasks quickly. It is not complete by any\n> stretch of the imagination. The user should be willing to look at the source code and possibly\n> use the cli to sqlite to massage the db if necessary.\n\n',
    'author': 'Michael MacKenna',
    'author_email': 'mpmackenna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
