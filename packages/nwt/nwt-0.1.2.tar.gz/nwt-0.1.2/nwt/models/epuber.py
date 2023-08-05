#! -*- coding: utf-8 -*-
"""
nwt.models.epuber
-----------------

Interact and scrap epub file.
"""

import zipfile
import functools
from logzero import logger as log
from bs4 import BeautifulSoup, NavigableString

from ..controllers.error import NwtWarning, InputError


def between(cur, end):
    """
    Get text between two different tag
    """

    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


def parse_int_list(range_string, delim=',', range_delim='-'):
    """
    Returns a sorted list of positive integers based on
    *range_string*. Reverse of :func:`format_int_list`.

    Args:
        range_string (str):
            String of comma separated positive integers or ranges
            (e.g. '1,2,4-6,8'). Typical of a custom page range string used
            in printer dialogs.

        delim (char):
            Defaults to ','. Separates integers and contiguous ranges of
            integers.

        range_delim (char):
            Defaults to '-'. Indicates a contiguous range of integers.

    >>> parse_int_list('1,3,5-8,10-11,15')
    [1, 3, 5, 6, 7, 8, 10, 11, 15]
    """
    output = []

    for element in range_string.strip().split(delim):

        # Range
        if range_delim in element:
            range_limits = list(map(int, element.split(range_delim)))
            output += list(range(min(range_limits), max(range_limits)+1))

        # Empty String
        elif not element:
            continue

        # Integer
        else:
            output.append(int(element))

    return sorted(output)


class Epub:
    def __init__(self, epub_file):
        if not zipfile.is_zipfile(epub_file):
            raise NwtWarning(f'Not a valid epub file: {epub_file}')

        self.zf = zipfile.ZipFile(epub_file, 'r')

        self.epub_file = epub_file

    @property
    def path(self):
        return self.epub_file.resolve()

    def read(self, file):
        return self.zf.read(file)

    def sread(self, file):
        """
        Read file and souped it.
        """
        return BeautifulSoup(self.read(f'OEBPS/{file}'), "html.parser")

    @property
    def toc(self):
        return self.sread('toc.xhtml')


class EpubBible(Epub):
    @property
    def title(self):
        return self.toc.head.title.text

    @property
    def stand(self):
        st = self.title.split('(')[-1]
        st = st.split(')')[0]
        return st.replace('-', '_')

    def parse(self, rawsubbook):
        subbook = dict()
        for raw in rawsubbook.split(';'):
            chapter = int(raw.split(':')[0])
            verset = parse_int_list(raw.split(':')[1])
            subbook[chapter] = verset

        return subbook

    def scrap(self, book_or_path, subbook):
        subbook = subbook if isinstance(subbook, dict) else self.parse(subbook)
        c = self.chapter_list(book_or_path)

        new_dict = dict()
        for chapter in subbook:
            try:
                v = self.verset_list(c[int(chapter) - 1])
            except IndexError:
                log.error(f'No such {int(chapter) - 1}')
                continue
            new_dict[chapter] = dict()
            for verset in subbook[chapter]:

                new_dict[chapter][verset] = v[int(verset) - 1]

        return new_dict

    @property
    @functools.lru_cache(maxsize=None)
    def book_list(self):
        bl = []
        rawlist = self.toc.body.section.nav.ol.find_all('a')[1:67]
        for element in rawlist:
            if 'Outline' not in element.text:
                bl.append({
                    'name': element.text,
                    'path': element.attrs['href'],
                })

        return bl

    @functools.lru_cache(maxsize=None)
    def chapter_list(self, book_or_path):
        if book_or_path in (map(lambda x: x['name'], self.book_list)):
            found = False
            i = 0
            while not found:
                if self.book_list[i]['name'] == book_or_path:
                    rcl = self.book_list[i]['path']
                    found = True
                else:
                    i += 1
        elif book_or_path in (map(lambda x: x['path'], self.book_list)):
            rcl = book_or_path
        else:
            raise InputError(f'"{book_or_path}" no found')

        lmn = self.sread(rcl).body.table.find_all('a')
        return list(map(lambda x: x.attrs['href'], lmn))

    @functools.lru_cache(maxsize=None)
    def verset_list(self, path):
        if 'split' in path:
            chap = path.split('.')[0].split('split')[-1]
        else:
            chap = '1'
        n, f = 1, []
        while True:
            tag = u"chapter{}_verse{}"
            start = tag.format(str(chap), str(int(n)))
            end = tag.format(str(chap), str(int(n) + 1))

            try:
                f.append(
                    ' '.join(
                        _ for _ in between(
                            self.sread(path).find("span", attrs={"id": start}).next_sibling,  # noqa
                            self.sread(path).find("span", attrs={"id": end}),
                        )
                    )
                )
                n += 1
            except AttributeError:
                break

        return f
