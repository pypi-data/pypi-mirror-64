#! -*- coding: utf-8 -*-
"""
nwt.views.console.command
-------------------------

Interact with user in console.
"""

from pathlib import Path

import cmd2
from pylev import damerau_levenshtein as lev

from ...models.epuber import EpubBible
from ...models.config import Config


class GetDistance(object):
    def __init__(self, enter):
        self.enter = enter
        self.distance = 0
        config = Config()
        epub_bible = EpubBible(config['active']['path'])
        book_list = epub_bible.book_list

        dist_list = list()
        for book in book_list:
            dist_list.append(lev(book['name'], self.enter))

        while True:
            try:
                self.closest = book_list[dist_list.index(self.distance)]['name']  # noqa
                break
            except ValueError:
                self.distance += 1

    @property
    def with_sub(self):
        return len(self.closest.split(' ')) > 1

    def __len__(self):
        return self.distance

    def __str__(self):
        return self.closest

    def __eq__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance == arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance == int(arg)
        else:
            return False

    def __ne__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance != arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance != int(arg)
        else:
            return False

    def __gt__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance > arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance > int(arg)
        else:
            return False

    def __ge__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance >= arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance >= int(arg)
        else:
            return False

    def __lt__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance < arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance < int(arg)
        else:
            return False

    def __le__(self, arg):
        if isinstance(arg, GetDistance):
            return self.distance <= arg.distance
        elif isinstance(arg, int) or isinstance(arg, float):
            return self.distance <= int(arg)
        else:
            return False


class InteractiveView(cmd2.Cmd):
    prompt = ' nwt > '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_postparsing_hook(self.command_space_hook)
        self.register_postparsing_hook(self.divide_pointer_hook)

    def do_clear(self, arg):

        with open(Path('./instance/result'), 'w') as fp:
            fp.write('')

    def command_space_hook(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:  # noqa
        cmd = data.statement.command
        arg = data.statement.args.split(' ')

        prebook1 = GetDistance(cmd)
        prebook2 = GetDistance(' '.join([cmd, arg[0]]))

        entbook = prebook1 if prebook1 <= prebook2 else prebook2

        if entbook.distance <= 2:
            if entbook.with_sub:
                data.statement = self.statement_parser.parse("{} {}".format(
                    entbook.closest.replace(' ', '_'),
                    ' '.join(arg[1:])
                ))
                return data
            else:
                data.statement = self.statement_parser.parse("{} {}".format(
                    entbook.closest,
                    ' '.join(arg)
                ))
                return data
        else:
            data.statement = self.statement_parser.parse("{} {}".format(
                cmd,
                ' '.join(arg)
            ))
            return data

    def divide_pointer_hook(self, data: cmd2.plugin.PostparsingData) -> cmd2.plugin.PostparsingData:  # noqa
        cmd = data.statement.command
        args = data.statement.args.split(' ')

        prebook1 = GetDistance(cmd)
        prebook2 = GetDistance(' '.join([cmd, args[0]]))

        entbook = prebook1 if prebook1 <= prebook2 else prebook2

        data.statement = self.statement_parser.parse("{} {}".format(
            cmd,
            ';'.join(args) if entbook <= 2 else ' '.join(args)
        ))
        return data
