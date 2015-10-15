# -*- coding: utf-8 -*-

import pytest


travis_lines = [
    'travis_fold:start:*',
    'travis_fold:end:*',
]


@pytest.fixture
def failtest(testdir):
    testdir.makepyfile("""
        def test_sth():
            print('boo!')
            assert False
    """)
    return testdir.runpytest


def test_no_travis_env(failtest, monkeypatch):
    """Check cmdline options on a dev env (no TRAVIS variable)."""
    monkeypatch.delenv('TRAVIS', raising=False)

    with pytest.raises(pytest.fail.Exception):
        failtest().stdout.fnmatch_lines(travis_lines)
    with pytest.raises(pytest.fail.Exception):
        failtest('--travis-fold=auto').stdout.fnmatch_lines(travis_lines)

    failtest('--travis-fold=always').stdout.fnmatch_lines(travis_lines)

    with pytest.raises(pytest.fail.Exception):
        failtest('--travis-fold=never').stdout.fnmatch_lines(travis_lines)


def test_travis_env(failtest, monkeypatch):
    """Set TRAVIS=true and check the stdout section is properly wrapped."""
    monkeypatch.setenv('TRAVIS', 'true')

    failtest().stdout.fnmatch_lines(travis_lines)
    failtest('--travis-fold=auto').stdout.fnmatch_lines(travis_lines)

    failtest('--travis-fold=always').stdout.fnmatch_lines(travis_lines)

    with pytest.raises(pytest.fail.Exception):
        failtest('--travis-fold=never').stdout.fnmatch_lines(travis_lines)
