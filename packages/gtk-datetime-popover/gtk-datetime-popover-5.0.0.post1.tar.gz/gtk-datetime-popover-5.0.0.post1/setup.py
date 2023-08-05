# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datetime_popover', 'datetime_popover.tests']

package_data = \
{'': ['*']}

install_requires = \
['pygobject>=3.34.0,<4.0.0']

setup_kwargs = {
    'name': 'gtk-datetime-popover',
    'version': '5.0.0.post1',
    'description': 'A Gtk Popover widget for handling dates and times',
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
