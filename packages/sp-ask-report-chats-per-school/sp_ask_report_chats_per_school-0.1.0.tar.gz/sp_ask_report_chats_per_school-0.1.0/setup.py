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
    'version': '0.1.0',
    'description': '',
    'long_description': '',
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
