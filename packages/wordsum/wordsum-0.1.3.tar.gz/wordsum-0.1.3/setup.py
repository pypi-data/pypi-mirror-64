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
    'version': '0.1.3',
    'description': 'Counting words within a folder of files recursively.',
    'long_description': '# Word Sum\n\nWordsum is a package for counting words within a folder of files recursively.\n\n## Usage\n\n``` python\nimport wordsum\n\nif __name__ == "__main__":\n    print(wordsum.count_words(\'./example_files\',[\'.md\',\'.ipynb\']))\n    wordsum.list_supported_formats()\n```\n\n## Installation\n\nIf you are using pip:\n\n    pip install wordsum\n\n## Supported Formats\n\nCurrently wordsum only supports markdown `.md` and jupyter notebooks `.ipynb`.\n\n## Contribute\n\nPRs are welcome for anything!',
    'author': 'JackMcKew',
    'author_email': 'jackmckew2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JackMcKew/wordsum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
