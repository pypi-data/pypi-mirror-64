# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_station']

package_data = \
{'': ['*'], 'fn_station': ['templates/*']}

install_requires = \
['apispec-webframeworks>=0.5.2,<0.6.0',
 'apispec>=3.3.0,<4.0.0',
 'flasgger',
 'fn_graph',
 'fn_graph_studio',
 'marshmallow-dataclass>=7.3.0,<8.0.0',
 'multi-dash',
 'psycopg2>=2.8.4,<3.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'fn-station',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
