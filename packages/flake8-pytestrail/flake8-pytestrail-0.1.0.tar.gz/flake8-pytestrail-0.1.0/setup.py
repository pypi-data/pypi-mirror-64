# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_pytestrail']
install_requires = \
['attrs>=19.2.0', 'flake8>=3.0.0']

entry_points = \
{'flake8.extension': ['TR = flake8_pytestrail:PyTestRailChecker']}

setup_kwargs = {
    'name': 'flake8-pytestrail',
    'version': '0.1.0',
    'description': 'Flake8 plugin to check for missing or wrong TestRail test identifiers',
    'long_description': '# flake8-pytestrail',
    'author': 'Andrey Semakin',
    'author_email': 'and-semakin@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/and-semakin/flake8-pytestrail',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
