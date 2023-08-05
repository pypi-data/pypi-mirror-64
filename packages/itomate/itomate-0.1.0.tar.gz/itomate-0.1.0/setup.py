# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['itomate']
install_requires = \
['iterm2>=1.11,<2.0', 'pyyaml>=3.11.1,<4.0.0']

entry_points = \
{'console_scripts': ['itomate = entry:main']}

setup_kwargs = {
    'name': 'itomate',
    'version': '0.1.0',
    'description': 'Automate your iTerm layouts and workflows',
    'long_description': None,
    'author': 'Kamran Ahmed',
    'author_email': 'kamranahmed.se@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
