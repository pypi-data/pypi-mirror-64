#! -*- coding: utf-8 -*-
"""
nwt.controllers.core
--------------------

Main engine of bible.
"""

from pathlib import Path

import cmd2
from bullet import Bullet
from bullet.client import keyhandler
from bullet.charDef import NEWLINE_KEY
from logzero import logger as log

from ..views.console.command import InteractiveView
from ..views.console.printer import render
from ..models.config import Config
from ..models.epuber import EpubBible


# - Console command - #
#######################
config = Config()
epub_bible = EpubBible(config['active']['path'])  # TODO: return None when not installed


class BulletItem(Bullet):

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        pos = self.pos
        ret = super(BulletItem, self).accept()
        return pos, ret


def wrap_book(name):
    @cmd2.with_category('Book')
    def ab_book(self, arg):
        log.debug(f'book: {name}')
        log.debug(f'pointer: {epub_bible.parse(arg)}')
        result = epub_bible.scrap(name, arg)
        self.poutput(render(result))

        if config['use_web']:
            choices = []
            v_list = []
            for chapter in result:
                for verset in result[chapter]:
                    v_list.append(result[chapter][verset])
                    choices.append(f"{name} {chapter}:{verset}")

            choices.append('end')
            cli = BulletItem(
                    prompt="Andininteny: ",
                    choices=choices,
                    indent=0,
                    align=5,
                    margin=2,
                    shift=0,
                    bullet=" > ",
                    pad_right=5
                )

            with open(Path('./instance/result'), 'w') as fp:
                fp.write(v_list[0])

            while True:
                pos, book = cli.launch()
                if book != 'end':
                    with open(Path('./instance/result'), 'w') as fp:
                        fp.write(v_list[pos])
                else:
                    break

    return ab_book


book_def = {}

for book in epub_bible.book_list:
    _name_ = f"do_{book['name'].replace(' ', '_')}"
    _func_ = wrap_book(book['name'])

    book_def[_name_] = _func_


Interactive = type("Interactive", (InteractiveView,), book_def)
