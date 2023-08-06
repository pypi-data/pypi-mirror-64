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
    'version': '0.2.0',
    'description': 'Dead-simple database migration with Yoyo for your Flask app',
    'long_description': "![Flask-Yoyo](https://gitlab.com/bersace/flask-yoyo/raw/master/docs/logo-horizontal.png?inline=false)\n\nDead-simple database migration for your Flask app with\n[Yoyo](https://ollycope.com/software/yoyo/latest/).\n\n\n## Features\n\n- Integration with Flask configuration.\n- Integration with Flask CLI.\n\n\n## Installation & Usage\n\nInstall it from PyPI:\n\n``` console\n$ pip install flask-yoyo\n```\n\nNow enable Yoyo using the extension on you app:\n\n``` python\nfrom flask_yoyo import Yoyo\n\nYoyo(app)\n```\n\nBy default, Flask-Yoyo stores migration in *migrations* folder side by side\nwith your you Flask app module. Flask-Yoyo reads `SQLALCHEMY_DATABASE_URI` to\nconfigure yoyo. You can override this by setting `YOYO_DATABASE_URI`.\n\nFlask-Yoyo is licensed under BSD.\n\n\n## Contribution & Support\n\nFlask-Yoyo home is it's project page on GitLab. Support is available throught\nissues. Contribution are welcome using Merge request.\n",
    'author': 'Étienne BERSAC',
    'author_email': 'bersace03@cae.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flask-yoyo',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
