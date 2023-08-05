# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

import tempfile
import shlex
from urllib.parse import urljoin

import requests
import bs4
import readability
import chardet

from wa.utils import safe_run


class WebExtractor:
    def __init__(self, url):
        self._url = url
        self._doc = None
        self._fetched = None

        resp = requests.get(self._url)
        self._fetched = to_utf(resp.content) or resp.text

    @property
    def doc(self):
        if self._doc is None:
            soup = bs4.BeautifulSoup(self._fetched, 'lxml')

            _urljoin(soup.find_all('img'), 'src', self._url)
            _urljoin(soup.find_all('a'), 'href', self._url)

            self._doc = readability.Document(str(soup.html))

        return self._doc

    @property
    def title(self):
        title = self.doc.short_title()
        if title:
            return title
        return title.split('/')[-1].split('?')[0]

    @property
    def html(self):
        return self.doc.summary()

    @property
    def md(self):
        cp = safe_run(['pandoc', '-f', 'html', '-t', 'commonmark'],
                      input=self.html, text=True, capture_output=True)
        if cp.returncode == 0:
            return cp.stdout
        return None

    @property
    def text(self):
        soup = bs4.BeautifulSoup(self.html, 'lxml')
        return soup.get_text()

    def original_dump(self, web_cmd):
        cmd = shlex.split(web_cmd)
        with tempfile.NamedTemporaryFile('w', suffix='.html') as f:
            f.write(self._fetched)
            f.flush()

            cmd.append('file://{}'.format(f.name))
            cp = safe_run(cmd, text=True, capture_output=True)
            if cp.returncode == 0:
                return cp.stdout
        return None


def to_utf(data):
    result = chardet.detect(data)
    if result['confidence'] > 0.80:
        return data.decode(result['encoding'], errors='replace')
    return None


def _is_relative_path(path):
    relative_paths = ('/', './', '../')
    return any(path.startswith(rp) for rp in relative_paths)


def _urljoin(tags, attr, url):
    for tag in tags:
        path = tag.get(attr, '')
        if _is_relative_path(path):
            tag[attr] = urljoin(url, path)
