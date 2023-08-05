# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

import os
import sys
import subprocess
import argparse
import tempfile
import shlex
import contextlib
from datetime import datetime as dt

from wa._version import version

class Article:
    def __init__(self):
        self.title = None
        self.text = None

    @property
    def initialized(self):
        return self.title and self.text


def eprint(*a, **kw):
    kw['file'] = sys.stderr
    print(*a, **kw)


def to_text_web(url, web_cmd):
    cmd = shlex.split(web_cmd)
    cmd.append(url)
    cp = subprocess.run(cmd, text=True, capture_output=True)

    out = Article()
    out.text = cp.stdout
    out.title = url.split('/')[-1].split('?')[0]
    return out


def to_text_readability(url):
    import newspaper
    article = newspaper.Article(url)
    article.download()
    article.parse()

    out = Article()
    out.text = article.text
    out.title = article.title
    return out


def to_mobi(url):
    import requests

    with tempfile.NamedTemporaryFile(suffix='.html') as tf:
        resp = requests.get(url)
        tf.write(resp.text)

        # requires Calibre
        subprocess.run(['ebook-convert', tf.name, 'document.mobi'])


def to_filename(title):
    return '{}.txt'.format(title.lower().replace(' ', '-'))


@contextlib.contextmanager
def make_printer(args):
    if args.save:
        with open(args.save, 'w') as f_:
            yield lambda *a: print(*a, file=f_)
    else:
        yield lambda *a: print(*a)


def prepare_args():
    parser = argparse.ArgumentParser(
        description='Fetch and parse web page and send it to kindle'
    )

    parser.add_argument('-s', '--save', nargs='?', const='', metavar='FILE',
        help='save the article to file instead of printing it to stdout. '
             'This option accepts a file path. If no path is provided, file '
             'name will be deduced from article title. Name of deduced file '
             'will be printed to stdout.')
    parser.add_argument('-t', '--title',
        help='set title of fetched article.')
    parser.add_argument('-m', '--front-matter', action='store_true',
        help='print YAML front matter with fetched metadata in front of '
             'article contents')
    parser.add_argument('--web', action='store_true',
        help='fetch the whole content of page instead of fetching only '
             'readable parts. This should be used as a fallback for pages '
             'which are incorrectly parsed and archived. Uses command from '
             '"--web-cmd" option.')
    parser.add_argument('--web-cmd', default='links -dump', metavar='CMD',
        help='uses this command + URL to fetch contents of web page when '
             '"--web" mode is used.')
    parser.add_argument('-f', '--force', action='store_true',
        help='forces overwriting output files.')
    parser.add_argument('--version', action='version',
                    version='%(prog)s {}'.format(version))
    parser.add_argument('url')
    return parser.parse_args()

def main():
    args = prepare_args()

    # fetch article's contents
    if args.web:
        article = to_text_web(args.url, args.web_cmd)
    else:
        article = to_text_readability(args.url)
        if not article.initialized:
            article = to_text_web(args.url, args.web_cmd)

    # overwrite title
    if args.title:
        article.title = args.title

    # deduce save file path
    savepath_deduced = (args.save == '')
    if args.save == '':
        args.save = to_filename(article.title)

    if args.save and os.path.exists(args.save) and not args.force:
        eprint('File exists, refusing overwriting: "{}"'.format(args.save))
        return 1

    with make_printer(args) as printer:
        if savepath_deduced:
            eprint(args.save)

        if args.front_matter:
            printer('---')
            printer('title:', article.title)
            printer('date:', dt.now().replace(microsecond=0).isoformat())
            printer('---')
            printer()
        printer(article.text)


sys.exit(main())
