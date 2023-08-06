# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_prometheus_exporter']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'prometheus_client>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'aiohttp-prometheus-exporter',
    'version': '0.1.0a2',
    'description': '',
    'long_description': None,
    'author': 'Adrian Krupa',
    'author_email': 'adrian.krupa91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
