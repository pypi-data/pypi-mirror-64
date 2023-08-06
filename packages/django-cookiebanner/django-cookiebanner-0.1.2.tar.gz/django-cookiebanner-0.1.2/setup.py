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
    'version': '0.1.2',
    'description': '',
    'long_description': '# Django-Cookiebanner\n\n## Installation\n\n`pip install django-cookiebanner`\n\n\n## Usage\n\n* Add `cookiebanner` to your `INSTALLED_APPS`\n\n* in your settings (`settings.py`) specify the different Cookie Groups:\n```python\nCOOKIEBANNER_GROUPS = [\n    {\n        "id": "essential",\n        "name": "Essential",\n        "description": "Essential cookies allow this page to work.",\n        "cookies": [\n            {"pattern": "cookiebanner", "description": "Meta cookie for the cookies that are set."},\n            {"pattern": "csrftoken", "description": "This cookie prevents Cross-Site-Request-Forgery attacks."},\n            {"pattern": "sessionid", "description": "This cookie is necessary to allow logging in, for example."},\n        ],\n    },\n    {\n        "id": "analytics",\n        "name": "Analytics",\n        "optional": True,\n        "cookies": [\n            {"pattern": "_pk_.*", "description": "Matomo cookie for website analysis."},\n        ],\n    },\n]\n```\n\n* In your base template add the banner and the conditionals:\n```djangotemplate\n{% load cookiebanner %}\n...\n<body>\n{% cookiebanner_modal %}\n...\n\n\n{% cookie_accepted \'analytics\' as cookie_analytics %}\n{% if cookie_analytics %}\n<script>... javascript for matomo ...</script>\n{% endif %}\n</body>\n```\n\n\n',
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
