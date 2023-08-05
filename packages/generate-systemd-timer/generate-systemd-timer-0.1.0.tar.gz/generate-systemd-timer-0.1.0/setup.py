# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['systemd_generator']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11,<3.0', 'python-editor>=1.0,<2.0']

entry_points = \
{'console_scripts': ['generate-systemd-timer = systemd_generator:main']}

setup_kwargs = {
    'name': 'generate-systemd-timer',
    'version': '0.1.0',
    'description': 'Generate a systemd unit.timer and unit.service pair',
    'long_description': None,
    'author': 'Thom Wiggers',
    'author_email': 'thom@thomwiggers.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
