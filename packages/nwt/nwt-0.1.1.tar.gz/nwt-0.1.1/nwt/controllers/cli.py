#! -*- coding: utf-8 -*-
"""
nwt.controllers.cli
-------------------

Interact with user in command line.
"""

import click
from logzero import logger as log

from .error import error_handler
from .setup import install as inst
from .setup import download as dl
from ..models import HOME_DIR
from ..models.config import Config
from ..models.epuber import EpubBible


@click.group(invoke_without_command=True)
@click.pass_context
@error_handler
def main(ctx):
    """
    NWT: Bible new world translation in cli
    """
    if ctx.invoked_subcommand is None:
        from .core import Interactive
        from ..views.console import greet
        log.debug('load config')
        config = Config()
        log.debug('config loaded')

        log.debug('load bible')
        epub_bible = EpubBible(config['active']['path'])
        log.debug('bible loaded')
        greet(epub_bible.title)

        session = Interactive(
            terminators=['\\'],
            persistent_history_file=HOME_DIR / 'history')
        session.debug = True
        session.cmdloop()


@main.command()
@click.option('-e', '--existing',
              type=click.Path(exists=True),
              help='Install an existing epub bible', )
@click.argument('bible', required=False)
@error_handler
def install(existing, bible):
    """
    Download and install bible.
    """
    if existing is not None:
        from pathlib import Path
        inst(Path(existing))
    else:
        from ..views.console.printer import bullet
        from ..models import bible_list
        bbl = bible if bible in bible_list else bullet('Choose Bible', list(bible_list.keys()))  # noqa
        downloaded = dl(bible_list[bbl]['link'])

        inst(downloaded)


@main.command()
@click.option('-e', '--edit',
              help='Open an editor to modify the specified config file')
@error_handler
def config():
    """
    Get and set nwt's options.
    """
    pass
