pytest-travis-fold
===================================

.. image:: https://travis-ci.org/abusalimov/pytest-travis-fold.svg?branch=master
    :target: https://travis-ci.org/abusalimov/pytest-travis-fold
    :alt: See Build Status on Travis CI

Folds captured output sections in Travis CI build log.

Installation and Usage
-----

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

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/abusalimov/pytest-travis-fold/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
