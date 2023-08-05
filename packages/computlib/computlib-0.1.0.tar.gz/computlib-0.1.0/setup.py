# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['computlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'computlib',
    'version': '0.1.0',
    'description': 'Simple mathematical library',
    'long_description': '#\xa0Computlib\n\nA simple compute library\n\n## Documentations\n\nSee [Documentation page](https://mlysakowski.gitlab.io/computlib/)',
    'author': 'Mathieu LYSAKOWSKI',
    'author_email': 'mathieu@phec.net',
    'maintainer': 'Mathieu LYSAKOWSKI',
    'maintainer_email': 'mathieu@phec.net',
    'url': 'https://gitlab.com/mlysakowski/computlib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
