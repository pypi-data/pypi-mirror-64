import pytest

from nwt.views.console.printer import render, Color, bullet


def test_render():
    obj = {
        '24': {
            '14': 'quatorz',
            '15': 'quize',
            '16': 'seize',
        }
    }
    assert '24' in render(obj)
    assert '15' in render(obj)
    assert 'quatorz' in render(obj)


def test_color():
    assert Color.red('rouge') == '\x1b[31mrouge\x1b[0m'
    assert Color.green('vert') == '\x1b[32mvert\x1b[0m'
    assert Color.blue('bleu') == '\x1b[34mbleu\x1b[0m'