# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sp_ask_report_chats_per_school']

package_data = \
{'': ['*']}

install_requires = \
['lh3api>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'sp-ask-report-chats-per-school',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Ask Schools\n\n[\n![PyPI](https://img.shields.io/pypi/v/sp_ask_report_chats_per_school.svg)\n![PyPI](https://img.shields.io/pypi/pyversions/sp_ask_report_chats_per_school.svg)\n![PyPI](https://img.shields.io/github/license/guinslym/sp_ask_report_chats_per_school.svg)\n](https://pypi.org/project/sp_ask_report_chats_per_school/)\n[![TravisCI](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school.svg?branch=master)](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school)\n\n\nThis package helps to filter Chats\n\n\n## Installation\n\n**Ask Schools** can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install sp_ask_report_chats_per_school\n```\n\n## Usage\n\n\nExample:\n\n```python\n\nfrom sp_ask_report_chats_per_school import get_nbr_of_chats_per_school_for_this_day\n\nchats_DataFrame = get_nbr_of_chats_per_school_for_this_day(year=2020, month=3, day=11)\nchats_DataFrame.to_excel("chats_per_school.xlsx", index=True)\n\n```\n\n## Code of Conduct\n\nEveryone interacting in the project\'s codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).\n',
    'author': 'Guinsly Mondesir',
    'author_email': 'guinslym@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guinslym/sp_ask_report_chats_per_school',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
