# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sp_ask_chats_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sp-ask-chats-utils',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Ask Schools\n\n[\n![PyPI](https://img.shields.io/pypi/v/sp_ask_chats_utils.svg)\n![PyPI](https://img.shields.io/pypi/pyversions/sp_ask_chats_utils.svg)\n![PyPI](https://img.shields.io/github/license/guinslym/sp_ask_chats_utils.svg)\n](https://pypi.org/project/sp_ask_chats_utils/)\n[![TravisCI](https://travis-ci.org/guinslym/sp_ask_chats_utils.svg?branch=master)](https://travis-ci.org/guinslym/sp_ask_chats_utils)\n\n\nThis package helps to filter Chats\n\n\n## Installation\n\n**Ask Schools** can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install sp_ask_chats_utils\n```\n\n## Usage\n\n\nExample:\n\n```python\n\nfrom sp_ask_chats_utils import remove_practice_queues\n\nchats = remove_practice_queues(chats):\n\n```\n\n## Code of Conduct\n\nEveryone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).\n",
    'author': 'Guinsly Mondesir',
    'author_email': 'guinslym@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guinslym/sp_ask_chats_utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
