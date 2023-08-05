# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_editor']

package_data = \
{'': ['*']}

install_requires = \
['gtk-datetime-popover>=6.0.0,<7.0.0',
 'gtk-recurrence-popover>=4.0.0,<5.0.0',
 'pycairo>=1.18,<2.0',
 'pygobject>=3.32.2,<4.0.0',
 'task-recurrence>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'gtk-task-editor',
    'version': '0.0.0',
    'description': 'A Gtk Dialog for todo apps that allows for viewing and editing individual tasks and todos',
    'long_description': None,
    'author': 'BeatLink',
    'author_email': 'beatlink@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
