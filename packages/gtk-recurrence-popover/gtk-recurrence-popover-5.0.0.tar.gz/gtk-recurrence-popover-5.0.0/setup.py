# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recurrence_popover', 'recurrence_popover.tests']

package_data = \
{'': ['*']}

install_requires = \
['gtk-datetime-popover>=6.0.0,<7.0.0',
 'pygobject>=3.32.2,<4.0.0',
 'task-recurrence>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'gtk-recurrence-popover',
    'version': '5.0.0',
    'description': 'A Gtk Popover for todo apps that allows you to select recurrence settings',
    'long_description': None,
    'author': 'BeatLink',
    'author_email': 'beatlink@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
