# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screenplay_pdf_to_fountain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'screenplay-pdf-to-fountain',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
