"""
nwt.models
----------

Model component of nwt.
"""

import os
from pathlib import Path


# Path
try:
    # for termux
    _PREFIX = Path(os.environ['PREFIX'])
except KeyError:
    _PREFIX = Path('/')
_HOME = Path(os.path.expanduser('~'))
HOME_DIR = _HOME / '.nwt/'
CACHE_DIR = _HOME / '.cache' / 'nwt/'
DOWNLOAD_DIR = CACHE_DIR / 'download/'
BIBLE_DIR = HOME_DIR / 'bible/'


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


for p in (CACHE_DIR, DOWNLOAD_DIR, BIBLE_DIR):
    mkdir(p)


def touch(fname, create_dirs: bool):
    if create_dirs:
        base_dir = os.path.dirname(fname)
        mkdir(base_dir)

    if not os.path.exists(fname):
        with open(fname, 'a'):
            os.utime(fname, None)


bible_link = 'https://download-a.akamaihd.net/files/media_publication'
bible_list = {
    'bi12_MG': {
        'lang': 'Malagasy',
        'link': f'{bible_link}/b1/bi12_MG.epub',
    },
    'nwt_E': {
        'lang': 'English',
        'link': f'{bible_link}/7d/nwt_E.epub',
    },
    'nwt_F': {
        'lang': 'Français',
        'link': f'{bible_link}/ec/nwt_F.epub',
    }
}
