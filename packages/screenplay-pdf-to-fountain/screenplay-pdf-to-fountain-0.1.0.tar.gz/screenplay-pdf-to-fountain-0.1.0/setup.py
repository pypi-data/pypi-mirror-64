# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screenplay_pdf_to_fountain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'screenplay-pdf-to-fountain',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
