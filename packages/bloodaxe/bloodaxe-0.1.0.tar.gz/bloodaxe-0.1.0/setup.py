# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bloodaxe']
install_requires = \
['httpx>=0.12.1,<0.13.0',
 'jinja2>=2.11.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10.0,<0.11.0',
 'typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['bloodaxe = bloodaxe:app']}

setup_kwargs = {
    'name': 'bloodaxe',
    'version': '0.1.0',
    'description': 'bloodaxe is the nice way to testing and metrifying api flows.',
    'long_description': '![bloodaxe logo](/images/logo.png)\n\n`bloodaxe` is the nice way to testing and metrify api flows.\n',
    'author': 'rfunix',
    'author_email': 'rafinha.unix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
