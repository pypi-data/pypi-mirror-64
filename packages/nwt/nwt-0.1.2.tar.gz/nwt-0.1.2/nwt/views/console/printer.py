#! -*- coding: utf-8 -*-
"""
nwt.views.console.printer
-------------------------

Print echo and show information in console.
"""

import click
import textwrap

from bullet import Bullet


def echo(*args, **kwargs):
    click.echo(*args, **kwargs)


def err(*args, **kwargs):
    echo(click.style(*args, **kwargs, fg='red'), err=True)


def bullet(prompt: str, choices: list):
    cli = Bullet(
            prompt=f"{prompt}: ",
            choices=choices,
            indent=0,
            align=5,
            margin=2,
            shift=0,
            bullet=" > ",
            pad_right=5
        )

    result = cli.launch()
    return result


class Color(object):
    def red(text):
        return click.style(str(text), fg='red')

    def green(text):
        return click.style(str(text), fg='green')

    def blue(text):
        return click.style(str(text), fg='blue')


def render(obj):
    '''
    obj
    ---
    '24': {
        '14': 'Ary hotoriana...',
        '15': 'noho izany...',
        '16': 'dia aoka izay...',
    }

    output
    ------
    24 14 Ary hotorina maneran-tany ity vaovao tsaran’ilay
     |  | fanjakana ity, ho vavolombelona amin’ny firenena rehetra,
     |  | vao ho tonga ny farany.
     | 15 noho izany
     | 16 dia aoka izany
    '''

    text = ''
    for chapter in obj:
        text += f'{Color.green(chapter)} '
        lenchapter = len(str(chapter))
        for verset in obj[chapter]:
            text += f'{Color.red(verset)} '
            lenverset = len(str(verset))
            wtext = textwrap.wrap(obj[chapter][verset], 60)
            for line in wtext:
                text += (line + '\n' + (' ' * lenchapter) + Color.green('|') +
                         (' ' * lenverset) + Color.red('|') + ' ')
            text += ('\n' + (' ' * lenchapter) +
                     Color.green('|') + ' ')
        text += ('\n' + (' ' * lenchapter))

    return '\n ' + text
