# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordsum', 'wordsum._file_types', 'wordsum._io', 'wordsum._util']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0', 'mypy>=0.770,<0.771', 'nbformat>=5.0.4,<6.0.0']

setup_kwargs = {
    'name': 'wordsum',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JackMcKew',
    'author_email': 'jackmckew2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
