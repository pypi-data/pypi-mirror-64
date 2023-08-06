# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stela']

package_data = \
{'': ['*']}

install_requires = \
['loguru', 'pyyaml', 'rootpath', 'scalpl', 'toml']

extras_require = \
{':python_version >= "3.6" and python_version < "4.0"': ['dataclasses']}

setup_kwargs = {
    'name': 'stela',
    'version': '1.0.0a1',
    'description': 'Find and read your project configuration files easily',
    'long_description': None,
    'author': 'Chris Maillefaud',
    'author_email': 'chrismaillefaud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
