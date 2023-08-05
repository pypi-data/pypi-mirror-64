# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slackdump']

package_data = \
{'': ['*']}

install_requires = \
['pyppeteer>=0.0.25,<0.0.26']

entry_points = \
{'console_scripts': ['slackdump = slackdump:cli']}

setup_kwargs = {
    'name': 'slackdump',
    'version': '0.0.1',
    'description': 'dump slack data',
    'long_description': None,
    'author': 'sloev',
    'author_email': 'johanned.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
