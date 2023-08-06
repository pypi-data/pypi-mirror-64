# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shotwell_mover']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['shotwell-mover = shotwell_mover.cli:main']}

setup_kwargs = {
    'name': 'shotwell-mover',
    'version': '0.2.0',
    'description': "Tool for changing paths of media stored in Shotwell's database",
    'long_description': "# shotwell-mover\n\nA tool for changing paths of media files stored in [Shotwell]'s database.\n\n[Shotwell]: https://wiki.gnome.org/Apps/Shotwell\n",
    'author': 'Tadej Janež',
    'author_email': 'tadej.j@nez.si',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tjanez/showell-mover',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
