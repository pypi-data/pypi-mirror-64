# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiebanner', 'cookiebanner.templatetags']

package_data = \
{'': ['*'], 'cookiebanner': ['templates/cookiebanner/*']}

install_requires = \
['django>=1.11']

setup_kwargs = {
    'name': 'django-cookiebanner',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Django-Cookiebanner\n\n## Installation\n\n`pip install django-cookiebanner`\n\n',
    'author': 'Andreas Nüßlein',
    'author_email': 'andreas@nuessle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
