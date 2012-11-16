Convertit
=========

A conversion webservice.

Idea is to make a GET request to the webservice and you ll get a downloadable transformed file:
Documents are pulled by the webserver.

GET parameters are:

- **url**: a url to a document to be grabbed from transformation
- **to**: output mimetype (optionnal, default to ``application/pdf`` if not provided)
- **from**: input mimetype (optionnal, guessed from input url if not provided)

Older transformed documents are cleaned after a defined time, tested at each http request on the application.

base transforms:
- odt -> pdf
- odt -> doc
- svg -> pdf

.. contents::

Feedback
========

Open an `Issue <https://github.com/makinacorpus/convertit/issues>`_ to report a bug or request a new feature.

Dependencies
============
* for OpenDocument support: unoconv
* for SVG support: inkscape

Install
=======
* Download and extract a released tarball from `pypi <http://pypi.python.org/pypi/convertit>`_
* The bleeding edge version is hosted on `github <https://github.com/makinacorpus/convertit>`_ ::

    git clone https://github.com/makinacorpus/convertit.git

* PreInstall it ::

    cd convertit
    python bootstrap.py -dc buildout-dev.cfg


Development
============
::

    cd convertit
    bin/buildout -Nc buildout-dev.cfg
    pserve --reload etc/wsgi/instance.ini

Run tests::

    bin/convertit.test

Once the application is running, you may visit http://localhost:6543/ in your browser.

Production
===========
::

    cd convertit
    cp local.cfg.in local.cfg
    $ED local.cfg
    bin/buildout -Nc buildout-prod.cfg
    bin/supervisord
    bin/supervisorctl status


Some files have been generated in etc/ for your convenience:

    * An init script
    * A logrotate configuration
    * An Apache vhost sample


Credits
========
Companies
---------
|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

Authors
------------
* Antoine Cezar
* Alex Marandon

Contributors
-----------------
* kiorky  <kiorky@cryptelium.net>


