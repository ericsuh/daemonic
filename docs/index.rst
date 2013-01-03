Welcome to the ``daemonic`` documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2

   api

Getting started
===============

``daemonic`` is pretty easy to use as a context manager::

    with daemonic.daemon(
            pidfile='/var/run/mydaemon.pid',
            stdout=open('/var/log/mydaemon.log', 'a')):
        # your daemon code here

``daemonic`` takes care of:

* Forking twice to detach from the current terminal/process
* Changing to a different working directory
* Managing user file creation permissions (``umask``)
* Redirecting standard input/output/error
* Creating a locked PID file

Licensing
=========

This code is freely licensed under the `MIT license
<http://opensource.org/licenses/MIT>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

