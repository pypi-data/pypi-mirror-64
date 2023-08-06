import logging
import os.path
import sys
from argparse import Namespace

import click
from flask import current_app
from flask.cli import FlaskGroup, with_appcontext
from yoyo import get_backend, read_migrations
from yoyo.config import get_configparser
from yoyo.scripts.newmigration import new_migration


logger = logging.getLogger(__name__)


class Yoyo:
    # The Flask extension.

    def __init__(self, app=None, sources=None):
        self.app = None
        if sources is None:
            import_mod = sys.modules[app.import_name]
            try:
                import_path = import_mod.__path__
            except AttributeError:
                import_path = os.path.dirname(import_mod.__file__)
            sources = [os.path.join(import_path, 'migrations')]
        self.sources = sources
        if app:
            self.init_app(app)

    def __repr__(self):
        return '<%s>' % (self.__class__.__name__,)

    def init_app(self, app):
        self.app = app
        app.yoyo = self
        uri = app.config.get(
            'YOYO_DATABASE_URI',
            app.config.get('SQLALCHEMY_DATABASE_URI')
        )
        self.backend = get_backend(uri)


@click.group()
@click.option("batch_mode", "-b", "--batch", is_flag=True,
              help="Run in batch mode. Turns off all user prompts")
@with_appcontext
def cli(**options):
    """Migrate database with Yoyo."""
    ctx = click.get_current_context()
    options['sources'] = current_app.yoyo.sources
    ctx.meta['flask_yoyo.root_options'] = options


@cli.command()
def apply():
    backend = current_app.yoyo.backend
    migrations = read_migrations(*current_app.yoyo.sources)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    logger.info("Database upgraded.")


@cli.command()
@click.option("-m", "--message", default="", help="Message")
@click.option("--sql", is_flag=True, help="Create file in SQL format")
def new(**options):
    ctx = click.get_current_context()
    options = dict(ctx.meta['flask_yoyo.root_options'], **options)
    args = Namespace(**options)
    config = get_configparser()
    new_migration(args, config)
