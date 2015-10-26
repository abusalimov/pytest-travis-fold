# -*- coding: utf-8 -*-
"""
Pytest plugin that folds captured output sections in Travis CI build log.
"""
from __future__ import absolute_import, division, print_function

import os
import re

from collections import defaultdict
from contextlib import contextmanager
from functools import partial, update_wrapper

import pytest
from py.builtin import _basestring


__author__ = "Eldar Abusalimov"
__version__ = "1.1.1"


PUNCT_RE = re.compile(r'\W+')


def normalize_name(name):
    """Strip out any "exotic" chars and whitespaces."""
    return PUNCT_RE.sub('-', name.lower()).strip('-')


def get_and_increment(name, counter=defaultdict(int)):
    """Allocate a new unique number for the given name."""
    n = counter[name]
    counter[name] = n + 1
    return n


def section_name(name, n, prefix='py-{pid}'.format(pid=os.getpid())):
    """Join arguments to get a Travis section name, e.g. 'py-123.section.0'"""
    return '.'.join(filter(bool, [prefix, name, str(n)]))


def section_marks(section, line_end=''):
    """A pair of start/end Travis fold marks."""
    return ('travis_fold:start:{0}{1}'.format(section, line_end),
            'travis_fold:end:{0}{1}'.format(section, line_end))


def new_section(name):
    """Create a new Travis fold section and return its name."""
    name = normalize_name(name)
    n = get_and_increment(name)
    return section_name(name, n)


def new_section_marks(name, line_end=''):
    """Create a new Travis fold section and return a pair of fold marks."""
    return section_marks(new_section(name), line_end)


def detect_nl(string_or_lines, line_end=None):
    """If needed, auto-detect line end using a given string or lines."""
    if line_end is None:
        line_end = '\n' if (string_or_lines and
                            string_or_lines[-1].endswith('\n')) else ''
    return line_end


class TravisContext(object):
    """Provides folding methods and manages whether folding is active.

    The precedence is (from higher to lower):

        1. The 'force' argument of folding methods
        2. The 'fold_enabled' attribute set from constructor
        3. The --travis-fold command line switch
        4. The TRAVIS environmental variable
    """

    def __init__(self, fold_enabled='auto'):
        super(TravisContext, self).__init__()
        self.setup_fold_enabled(fold_enabled)

    def setup_fold_enabled(self, value='auto'):
        if isinstance(value, _basestring):
            value = {
                'never': False,
                'always': True,
            }.get(value, os.environ.get('TRAVIS') == 'true')

        self.fold_enabled = bool(value)

    def is_fold_enabled(self, force=None):
        if force is not None:
            return bool(force)
        return self.fold_enabled

    def fold_lines(self, lines, name='', line_end=None, force=None):
        """Return a list of given lines wrapped with fold marks.

        If 'line_end' is not specified it is determined from the last line
        given.

        It is designed to provide an adequate result by default. That is, the
        following two snippets::

            print('\\n'.join(fold_lines([
                'Some lines',
                'With no newlines at EOL',
            ]))

        and::

            print(''.join(fold_lines([
                'Some lines\\n',
                'With newlines at EOL\\n',
            ]))

        will both output a properly folded string::

            travis_fold:start:...\\n
            Some lines\\n
            ... newlines at EOL\\n
            travis_fold:end:...\\n

        """
        if not self.is_fold_enabled(force):
            return lines
        line_end = detect_nl(lines, line_end)
        start_mark, end_mark = new_section_marks(name, line_end)
        ret = [start_mark, end_mark]
        ret[1:1] = lines
        return ret


    def fold_string(self, string, name='', sep='', line_end=None, force=None):
        """Return a string wrapped with fold marks.

        If 'line_end' is not specified it is determined in a similar way as
        described in docs for the fold_lines() function.
        """
        if not self.is_fold_enabled(force):
            return string
        line_end = detect_nl(string, line_end)
        if not (sep or line_end and string.endswith(line_end)):
            sep = '\n'
        return sep.join(self.fold_lines([string], name,
                                        line_end=line_end, force=force))


    @contextmanager
    def folding_output(self, name='', writeln=print, line_end='', force=None):
        """Makes the output be folded by the Travis CI build log view.

        Context manager that wraps the output with special 'travis_fold' marks
        recognized by Travis CI build log view.

        If 'writeln' doesn't append a newline char by itself
        ('sys.stdout.write' is an example), you must pass line_end='\\n'
        explicitly.
        """
        if not self.is_fold_enabled(force):
            yield
            return

        start_mark, end_mark = new_section_marks(name, line_end)

        writeln(start_mark)
        try:
            yield
        finally:
            writeln(end_mark)


def pytest_addoption(parser):
    group = parser.getgroup('Travis CI')
    group.addoption('--travis-fold',
        action='store', dest='travis_fold',
        choices=['never', 'auto', 'always'],
        nargs='?', default='auto', const='always',
        help='Fold captured output sections in Travis CI build log'
    )


@pytest.mark.trylast  # to let 'terminalreporter' be registered first
def pytest_configure(config):
    travis = TravisContext(config.option.travis_fold)

    reporter = config.pluginmanager.getplugin('terminalreporter')
    if travis.fold_enabled and hasattr(reporter, '_outrep_summary'):

        def patched_outrep_summary(rep):
            """Patched _pytest.terminal.TerminalReporter._outrep_summary()."""
            rep.toterminal(reporter._tw)
            for secname, content in rep.sections:
                name = secname

                # Shorten the most common case:
                # 'Captured stdout call' -> 'stdout'.
                if name.startswith('Captured '):
                    name = name[len('Captured '):]
                if name.endswith(' call'):
                    name = name[:-len(' call')]

                if content[-1:] == "\n":
                    content = content[:-1]

                with travis.folding_output(name,
                        writeln=reporter._tw.write, line_end='\n',
                        # Don't fold if there's nothing to fold.
                        force=(False if not content else None)):

                    reporter._tw.sep("-", secname)
                    reporter._tw.line(content)

        reporter._outrep_summary = update_wrapper(patched_outrep_summary,
                                                  reporter._outrep_summary)


@pytest.fixture(scope='session')
def travis(pytestconfig):
    """Methods for folding the output on Travis CI.

    * travis.fold_string()     -> string that will appear folded in the Travis
                                  build log
    * travis.fold_lines()      -> list of lines wrapped with the proper Travis
                                  fold marks
    * travis.folding_output()  -> context manager that makes the output folded
    """
    return TravisContext(pytestconfig.option.travis_fold)
