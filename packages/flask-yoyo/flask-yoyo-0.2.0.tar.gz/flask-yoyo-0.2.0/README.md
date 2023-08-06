![Flask-Yoyo](https://gitlab.com/bersace/flask-yoyo/raw/master/docs/logo-horizontal.png?inline=false)

Dead-simple database migration for your Flask app with
[Yoyo](https://ollycope.com/software/yoyo/latest/).


## Features

- Integration with Flask configuration.
- Integration with Flask CLI.


## Installation & Usage

Install it from PyPI:

``` console
$ pip install flask-yoyo
```

Now enable Yoyo using the extension on you app:

``` python
from flask_yoyo import Yoyo

Yoyo(app)
```

By default, Flask-Yoyo stores migration in *migrations* folder side by side
with your you Flask app module. Flask-Yoyo reads `SQLALCHEMY_DATABASE_URI` to
configure yoyo. You can override this by setting `YOYO_DATABASE_URI`.

Flask-Yoyo is licensed under BSD.


## Contribution & Support

Flask-Yoyo home is it's project page on GitLab. Support is available throught
issues. Contribution are welcome using Merge request.
