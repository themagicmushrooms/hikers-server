Hikers Log server
=================

Installation
------------

Requirements:

* Python 2.7.4 + dev (ubuntu package: python-dev)
* PostgreSQL (ubuntu packages: postgresql postgresql-server-dev-?.?)
* Postgis (ubuntu packages: postgresql-9.1-postgis)
* ubuntu package: daemontools (for "envdir")
* ubuntu package: pyflakes (for "flake8")
* ubuntu package: virtualenvwrapper (for "mkvirtualenv") (reopen a new shell after install)
* ubuntu package: libgeos-c1
* for "pillow", maybe some more native libs for image formats supports, check the setup summary is like the following (in pip output)::

    SETUP SUMMARY (Pillow 1.7.8 / PIL 1.1.7)
    --------------------------------------------------------------------
    version      1.7.8
    platform     linux2 2.7.4 (default, Apr 19 2013, 18:28:01)
                 [GCC 4.7.3]
    --------------------------------------------------------------------
    *** TKINTER support not available
    
    --- JPEG support available
    --- ZLIB (PNG/ZIP) support available
    --- FREETYPE2 support available
    *** LITTLECMS support not available


Getting the code::

    git clone https://github.com/themagicmushrooms/hikers-server
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

Here is a bash command to show the current values::

    (cd envdir/ && for i in *; do echo $i = $(cat $i) ; done)


Create a super user in postgres::

    # inspired by http://obroll.com/how-to-reset-postgres-password-in-postgresql-ubuntu-11-10-oneiric/
    sudo su postgres
       psql
          ALTER USER postgres WITH PASSWORD '123';

Create the db in postgres and upgrate it with postgis (adapt paths if needed)::

    for dbname in hikers template_postgis
    do
        sudo -u postgres createdb $dbname
        sudo -u postgres psql -d $dbname -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
        sudo -u postgres psql -d $dbname -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
    done

Note that if you drop and recreate the hikers database later, you can just call::

    createdb -U postgres -T template_postgis hikers

"Sync" the db (django)::

    make syncdb
    make user
       # enter a mail for your admin user and a password

Development
-----------

Listing available commands::

    make <tab>

Before commiting anything, make sure to:

Run the tests::

    make test

Run the source code checker::

    flake8

The Django debug toolbar is enabled when the ``DEBUG`` environment variable is
true and the ``django-debug-toolbar`` package is installed.

Environment variables for development are set in the ``envdir`` directory. For
tests, they are located in the ``tests/envdir`` directory.
