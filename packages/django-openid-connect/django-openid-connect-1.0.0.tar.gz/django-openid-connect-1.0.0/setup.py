# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_openid_connect']

package_data = \
{'': ['*']}

install_requires = \
['django-rest-framework-social-oauth2==1.1.0']

setup_kwargs = {
    'name': 'django-openid-connect',
    'version': '1.0.0',
    'description': 'Django library providing OpenID Connect auth backend',
    'long_description': None,
    'author': 'Miroslav Bauer',
    'author_email': 'bauer@cesnet.cz',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
