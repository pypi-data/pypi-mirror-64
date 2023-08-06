# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flask_yoyo']
install_requires = \
['flask>=1.1.1,<2.0.0', 'yoyo-migrations>=7.0.2,<8.0.0']

entry_points = \
{'flask.commands': ['yoyo = flask_yoyo:cli']}

setup_kwargs = {
    'name': 'flask-yoyo',
    'version': '0.1.0',
    'description': 'Dead-simple database migration with Yoyo for your Flask app',
    'long_description': None,
    'author': 'Étienne BERSAC',
    'author_email': 'bersace03@cae.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
