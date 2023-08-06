# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['structlog_to_seq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'structlog-to-seq',
    'version': '0.2.1',
    'description': 'A collection of structlog processors for using structlog with Seq log server',
    'long_description': None,
    'author': 'Gergő Jedlicska',
    'author_email': 'gergo@jedlicska.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
