kotti_bstable
******************
BootstrapTable support for Kotti

|pypi|_
|downloads_month|_
|license|_
|build_status_stable|_

.. |pypi| image:: https://img.shields.io/pypi/v/kotti_bstable.svg?style=flat-square
.. _pypi: https://pypi.python.org/pypi/kotti_bstable/

.. |downloads_month| image:: https://img.shields.io/pypi/dm/kotti_bstable.svg?style=flat-square
.. _downloads_month: https://pypi.python.org/pypi/kotti_bstable/

.. |license| image:: https://img.shields.io/pypi/l/kotti_bstable.svg?style=flat-square
.. _license: http://www.repoze.org/LICENSE.txt

.. |build_status_stable| image:: https://img.shields.io/travis/jamaicanDevelopers/kotti_bstable/production.svg?style=flat-square
.. _build_status_stable: http://travis-ci.org/jamaicanDevelopers/kotti_bstable

`Find out more about Kotti`_

Development happens at https://github.com/jamaicanDevelopers/kotti_bstable

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_bstable.kotti_configure

Database upgrade
===================

If you are upgrading from a previous version you might have to migrate your
database.  The migration is performed with `alembic`_ and Kotti's console script
``kotti-migrate``. To migrate, run
``kotti-migrate upgrade --scripts=kotti_bstable:alembic``.

For integration of alembic in your environment please refer to the
`alembic documentation`_. If you have problems with the upgrade,
please create a new issue in the `tracker`_.

Development
=============

|build_status_master|_

.. |build_status_master| image:: https://img.shields.io/travis/jamaicanDevelopers/kotti_bstable/master.svg?style=flat-square
.. _build_status_master: http://travis-ci.org/jamaicanDevelopers/kotti_bstable

Contributions to kotti_bstable are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: https://alembic.readthedocs.io/en/latest/index.html
.. _tracker: https://github.com/jamaicanDevelopers/kotti_bstable/issues
.. _Github repository: https://github.com/jamaicanDevelopers/kotti_bstable
