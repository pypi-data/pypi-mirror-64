"""
nwt.views.console
-----------------

App for console.
"""

import os
import logging

import logzero

from .printer import echo

from nwt import __version__


try:
    WIDTH = os.get_terminal_size()[0]
except OSError:
    WIDTH = 0


def greet(title=None):
    title = title or 'bible new world translation'
    s_version = 'Version: ' + __version__

    echo('-' * WIDTH)
    echo()
    echo(title.center(WIDTH))
    echo(s_version.center(WIDTH))
    echo()
    echo('-' * WIDTH)


_log_format = "%(color)s%(levelname)s:%(end_color)s %(message)s"
_formatter = logzero.LogFormatter(fmt=_log_format)
_log_level = logging.DEBUG

# Set up a temporary logger with default log level so that
# it can be used before log level argument is determined
logzero.setup_default_logger(formatter=_formatter, level=_log_level)
