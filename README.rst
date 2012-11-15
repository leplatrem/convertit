Convertit
=========

A conversion webservice.

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
* The bleeding edge version is hosted on github ::

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
    bin/scripts setup.py test

Once the application is running, you may visit http://localhost:6543/ in your browser.

Production
===========
::
    cd convertit
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


