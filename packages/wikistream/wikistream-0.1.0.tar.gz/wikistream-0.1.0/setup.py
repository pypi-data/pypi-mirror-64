# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikistream']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'aiosseclient>=0.0.1,<0.0.2',
 'psycopg2>=2.8.4,<3.0.0',
 'sqlalchemy>=1.3.15,<2.0.0']

setup_kwargs = {
    'name': 'wikistream',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jonan Scheffler',
    'author_email': 'jonanscheffler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
