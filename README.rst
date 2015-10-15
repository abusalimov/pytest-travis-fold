==================
pytest-travis-fold
==================

`Pytest`_ plugin that folds captured output sections in Travis CI build log.

.. image:: https://cloud.githubusercontent.com/assets/530396/10524841/52ecb102-738a-11e5-83ab-f3cf1b3316fb.png
    :alt: Travis CI build log view

Installation and Usage
----------------------

Just install the ``pytest-travis-fold`` package as part of your Travis CI build
by adding the following install step to the ``.travis.yml`` file::

    install:
      - pip install pytest-travis-fold

Output folding is enabled automatically by checking the presence of the
``TRAVIS`` environmental variable.

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

.. _MIT: http://opensource.org/licenses/MIT
.. _file an issue: https://github.com/abusalimov/pytest-travis-fold/issues
.. _Pytest: https://github.com/pytest-dev/pytest
.. _tox: https://tox.readthedocs.org/en/latest/
.. _PyPI: https://pypi.python.org/pypi
