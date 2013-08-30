Hikers Log server
=================

Installation
------------

Requirements:

* Python 2.7.4
* PostgreSQL
* ubuntu package: daemontools (for "envdir")
* ubuntu package: virtualenvwrapper (for "mkvirtualenv") (reopen a new shell after install)

Getting the code::

    git clone https://github.com/creynaud/hikers-server
    cd hikers-server
    mkvirtualenv -p python2.7 hikers-server
    add2virtualenv .
    pip install -r requirements-dev.txt

Configuration
-------------

The hikers server relies on environment variables for its configuration. The required environment variables are:

* ``DJANGO_SETTINGS_MODULE``: set it to ``hikers.settings``.
* ``SECRET_KEY``: set to a long random string.
* ``ALLOWED_HOSTS``: space-separated list of hosts which serve the web app.
  E.g. ``www.hikerslog.com hikerslog.com``.
* ``FROM_EMAIL``: the email address that sends automated emails (password
  lost, etc.). E.g. ``Hikers Log <info@hikerslog.com>``.
* ``REDIS_URL``: a URL for configuring redis. E.g.
  ``redis://localhost:6354/1``.
* ``DATABASE_URL``: a heroku-like database URL. E.g.
  ``postgres://user:password@host:port/database``.

Optionally you can customize:

* ``DEBUG``: set it to a non-empty value to enable the Django debug mode.

Here is a bash command to show the current values:

    (cd envdir/ && for i in *; do echo $i = $(cat $i) ; done)

Development
-----------

Before commiting anything, make sure to:

Run the tests::

    make test

Run the source code checker::

    flake8

The Django debug toolbar is enabled when the ``DEBUG`` environment variable is
true and the ``django-debug-toolbar`` package is installed.

Environment variables for development are set in the ``envdir`` directory. For
tests, they are located in the ``tests/envdir`` directory.
