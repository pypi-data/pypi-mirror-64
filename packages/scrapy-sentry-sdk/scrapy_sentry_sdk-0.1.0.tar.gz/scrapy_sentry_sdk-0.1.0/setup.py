# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrapy_sentry_sdk']

package_data = \
{'': ['*']}

install_requires = \
['scrapy>=1.6,<2.0', 'sentry-sdk>=0.14.3,<0.15.0']

setup_kwargs = {
    'name': 'scrapy-sentry-sdk',
    'version': '0.1.0',
    'description': 'Scrapy extension for integration of Sentry SDK to Scrapy projects',
    'long_description': None,
    'author': 'KristobalJunta',
    'author_email': 'junta.kristobal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
