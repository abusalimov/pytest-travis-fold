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


__author__ = "Eldar Abusalimov"


PUNCT_RE = re.compile(r'\W+')


class TravisContext(object):
    def __init__(self):
        super(TravisContext, self).__init__()

        self.section_stack = ['pytest-{pid}'.format(pid=os.getpid())]
        self.section_counter = defaultdict(int)

    @contextmanager
    def fold(self, tw, name):
        """Makes the output be folded by the Travis CI build log view.

        Context manager that wraps the output of the 'tw' TerminalWriter with
        special 'travis_fold' marks recognized by Travis CI build log view.
        """

        # Normalize name by stripping out any "exotic" chars.
        name = name.lower()
        if name.startswith('captured '):
            name = name[len('captured '):]
        name = PUNCT_RE.sub('-', name).strip('-')

        n = self.section_counter[name]
        self.section_counter[name] += 1

        self.section_stack.append('{0}-{n}'.format(name, n=n))
        try:
            section = '.'.join(self.section_stack)
            tw.line('travis_fold:start:%s' % section)
            try:
                yield
            finally:
                tw.line('travis_fold:end:%s' % section)
        finally:
            self.section_stack.pop()


travis = TravisContext()  # global singleton


def TerminalReporter__outrep_summary(self, rep):
    """Patched _pytest.terminal.TerminalReporter._outrep_summary() method."""
    rep.toterminal(self._tw)
    for secname, content in rep.sections:
        with travis.fold(self._tw, secname):  # <- this is what we add
            self._tw.sep("-", secname)
            if content[-1:] == "\n":
                content = content[:-1]
            self._tw.line(content)


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
    fold = {
        'never': False,
        'always': True,
    }.get(config.option.travis_fold, os.environ.get('TRAVIS') == 'true')

    if fold:
        reporter = config.pluginmanager.getplugin('terminalreporter')
        if hasattr(reporter, '_outrep_summary'):
            patched_outrep_summary = partial(TerminalReporter__outrep_summary,
                                             reporter)  # bind the self arg
            reporter._outrep_summary = update_wrapper(patched_outrep_summary,
                                                      reporter._outrep_summary)
