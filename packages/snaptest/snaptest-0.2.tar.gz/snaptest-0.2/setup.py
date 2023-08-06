# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snaptest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snaptest',
    'version': '0.2',
    'description': '',
    'long_description': None,
    'author': 'Michael Elsdörfer',
    'author_email': 'michael@elsdoerfer.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
