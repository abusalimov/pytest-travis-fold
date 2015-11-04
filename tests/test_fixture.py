# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys
from fnmatch import fnmatchcase

import pytest


travis_lines = [
    'travis_fold:start:*',
    'travis_fold:end:*',
]


def test_travis_fixture_registered(testdir):
    testdir.runpytest('--fixtures').stdout.fnmatch_lines([
        'travis',
    ])


@pytest.mark.parametrize('force', [True, False])
def test_is_fold_enabled(testdir, force):
    testdir.makepyfile("""
        def test_sth(travis):
            assert travis.is_fold_enabled(True) == True
            assert travis.is_fold_enabled(False) == False
            assert travis.is_fold_enabled() == {0!r}
    """.format(force))

    result = testdir.runpytest('--travis-fold={0}'
                               .format('always' if force else 'never'))
    assert result.ret == 0


@pytest.fixture(scope='module')
def travis_force(request, travis):
    saved_fold_enabled = travis.fold_enabled
    @request.addfinalizer
    def restore_fold_enabled():
        travis.fold_enabled = saved_fold_enabled

    travis.fold_enabled = True
    return travis


def assert_lines_folded(lines, line_end=''):
    assert lines
    marks = start, end = lines[0], lines[-1]

    if line_end:
        assert all(mark.endswith(line_end) for mark in marks)
    else:
        assert all(not mark.endswith('\n') for mark in marks)

    assert all(fnmatchcase(mark, pat)
               for mark, pat in zip(marks, travis_lines))


def assert_string_folded(string, line_end=''):
    assert string

    if line_end:
        assert string.endswith(line_end)
    else:
        assert not string.endswith('\n')

    string_lines = string.splitlines()
    if all(string_lines[1:-1]):
        assert '\n\n' not in string

    assert_lines_folded(string_lines)


def test_fold_lines(travis_force):
    assert_lines_folded(travis_force.fold_lines([], line_end='\n'), '\n')
    assert_lines_folded(travis_force.fold_lines([''], line_end='\n'), '\n')
    assert_lines_folded(travis_force.fold_lines(['\n'], line_end=''))
    assert_lines_folded(travis_force.fold_lines(['Aww!'], line_end='\n'), '\n')
    assert_lines_folded(travis_force.fold_lines(['Aww!\n'], line_end=''))


def test_fold_lines_detect_nl(travis_force):
    assert_lines_folded(travis_force.fold_lines([]))
    assert_lines_folded(travis_force.fold_lines(['']))
    assert_lines_folded(travis_force.fold_lines(['\n']), '\n')
    assert_lines_folded(travis_force.fold_lines(['Aww!']))
    assert_lines_folded(travis_force.fold_lines(['Aww!\n']), '\n')


def test_fold_string(travis_force):
    assert_string_folded(travis_force.fold_string('', line_end='\n'), '\n')
    assert_string_folded(travis_force.fold_string('\n', line_end=''))
    assert_string_folded(travis_force.fold_string('Woo!', line_end='\n'), '\n')
    assert_string_folded(travis_force.fold_string('Woo!\n', line_end=''))


def test_fold_string_detect_nl(travis_force):
    assert_string_folded(travis_force.fold_string(''))
    assert_string_folded(travis_force.fold_string('\n'), '\n')
    assert_string_folded(travis_force.fold_string('Woo!'))
    assert_string_folded(travis_force.fold_string('Woo!\n'), '\n')


def test_folding_output(travis_force, capsys):
    with travis_force.folding_output():
        print('Ouu!')
    with travis_force.folding_output(file=sys.stderr):
        print('Errr!', file=sys.stderr)

    out, err = capsys.readouterr()

    assert_string_folded(out, '\n')
    assert_string_folded(err, '\n')

