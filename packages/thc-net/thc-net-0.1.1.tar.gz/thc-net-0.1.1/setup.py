# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['thc_net']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=0.22.2,<0.23.0',
 'tensorflow-addons>=0.8.3,<0.9.0',
 'tensorflow>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'thc-net',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Hartorn',
    'author_email': 'hartorn.github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
