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
    'version': '0.1.1',
    'description': 'Generate a systemd unit.timer and unit.service pair',
    'long_description': "# Systemd generator for timer units\n\nGenerates systemd `.timer` and `.service` units to more easily add cron-like tasks to your system.\n\nYou'll still have to copy them into the right place (either `/etc/systemd/system`\nor `$HOME/.config/systemd/user`) and reload systemd using `systemctl daemon-reload`.\n\n## Usage\n\n```sh\ngenerate-systemd-timer unit-name\n# Now two editors will pop up to allow you to customize\n# Afterwards you'll find unit-name.service and unit-name.timer in the current folder.\n```\n",
    'author': 'Thom Wiggers',
    'author_email': 'thom@thomwiggers.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomwiggers/systemd-timer-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
