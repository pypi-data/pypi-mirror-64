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
    'version': '0.0.5',
    'description': 'dump slack data',
    'long_description': '# Slack Dump\n\n[![Latest Version](https://img.shields.io/pypi/v/slackdump.svg)](https://pypi.python.org/pypi/slackdump)\n\nDump slack data via chrome browser, and do analytics on it\n\n* [scraper.py](slackdump/scraper.py) scrapes a slack channel\n* [chrome.py](slackdump/chrome.py) starts a temporary chrome process on osx\n\n\n## Install\n\n```bash\n$ pip install slackdump\n```\n\n## Usage\n\nBefore running the `slackdump` command you need to\n\n* be logged into slack in chrome\n* close chrome completely\n\n**for osx**\n\n```bash\n$ slackdump --ROOTURL=https://somewhere.slack.com/messages/66666666 > output.json\n```\n\n',
    'author': 'sloev',
    'author_email': 'johanned.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sloev/slackdump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
