# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_prometheus_exporter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiohttp-prometheus-exporter',
    'version': '0.1.0a1',
    'description': '',
    'long_description': None,
    'author': 'Adrian Krupa',
    'author_email': 'adrian.krupa91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
