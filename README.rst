==================
pytest-travis-fold
==================

`Pytest`_ plugin that folds captured output sections in Travis CI build log.

.. image:: https://cloud.githubusercontent.com/assets/530396/10524841/52ecb102-738a-11e5-83ab-f3cf1b3316fb.png
    :alt: Travis CI build log view

Installation and Usage
----------------------

Just install the `pytest-travis-fold`_ package as part of your build.

When using `tox`_, add the package to the ``deps`` list in your ``tox.ini``
and make sure the ``TRAVIS`` environment variable is passed::

    [testenv]
    deps =
        pytest-travis-fold
    passenv = TRAVIS

If you **don't** use tox and invoke ``py.test`` directly from ``.travis.yml``,
you may install the package as an additional ``install`` step::

    install:
      - pip install -e .
      - pip install pytest-travis-fold

    script: py.test

Output folding is enabled automatically when running inside Travis CI. It is OK
to have the plugin installed also in your dev environment: it is only activated
by checking the presence of the ``TRAVIS`` environmental variable, unless the
``--travis-fold`` command line switch is used.


The ``travis`` fixture
----------------------
The plugin by itself only makes the captured output sections appear folded.
If you wish to make the same thing with arbitrary lines, you can do it manually
by using the ``travis`` fixture.

It is possible to fold the output of a certain code block using the
``travis.folding_output()`` context manager::

	def test_something(travis):
		with travis.folding_output():
			print('Lines, lines, lines...')
			print('Lots of them!')
			...

Or you may want to use lower-level ``travis.fold_string()`` and
``travis.fold_lines()`` functions and then output the result as usual.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-travis-fold" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _pytest-travis-fold: https://pypi.python.org/pypi/pytest-travis-fold
.. _MIT: http://opensource.org/licenses/MIT
.. _file an issue: https://github.com/abusalimov/pytest-travis-fold/issues
.. _Pytest: https://github.com/pytest-dev/pytest
.. _tox: https://tox.readthedocs.org/en/latest/
.. _PyPI: https://pypi.python.org/pypi
