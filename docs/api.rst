``daemonic`` API
================

``daemonic`` module
-------------------

.. py:module:: daemonic
.. py:currentmodule:: daemonic

.. py:class:: daemonic.daemon([pidfile=None, workingdir='/', umask=0, \
    stdin=None, stdout=None, stderr=None,])

    Context manager for POSIX daemon processes.

    :param pidfile: filepath for PID file.
    :type pidfile: string
    :param workingdir: path for daemon's working directory.
    :type pidfile: string
    :param umask: Permissions mask for daemon process.
    :type umask: int
    :param stdin: File from which to read standard input.
    :type stdin: File-like object
    :param stdout: File to which to write standard output.
    :type stdout: File-like object
    :param stderr: File to which to write standard error (if ``None``,
        defaults to same as ``stdout``).
    :type stderr: File-like object

    .. py:function:: daemonize()

        Make a daemon process and create its PID file.

        Calling this is normally unnecessary, as it is called for you when
        entering the managed context.

    .. py:function:: stop()

        Clean up a daemon process and delete its PID file.

        Calling this is normally unnecessary, as it is called for you when
        exiting the managed context.

``pidfile`` Module
------------------

Functions for managing PID files. You can use either the
:py:func:`pidfile` context manager or manually use
:py:func:`make_pidfile` and :py:func:`remove_pidfile` pair of functions.

.. py:module:: pidfile
.. py:currentmodule:: pidfile

.. py:function:: pidfile(path, pid)

    Context manager for using PID files. Essentially just calls
    :py:func:`make_pidfile` and :py:func:`remove_pidfile` before and after the
    entered block, respectively.

    :param path: filepath at which to create PID file.
    :type path: string
    :param pid: PID to write to the PID file.
    :type pid: int or string

.. py:function:: make_pidfile(path, pid)

    Creates a PID file at the given path. If a stale PID file exists at the
    path (as determined by :py:func:`pidfile_is_stale`), ``make_pidfile``
    will overwrite the file.

    :param path: filepath at which to create PID file.
    :type path: string
    :param pid: PID to write to the PID file.
    :type pid: int or string
    :raises: :py:class:`PIDFileError` if PID file exists at path and is not \
        stale.

.. py:function:: is_pid_running(pid)

    Checks if given PID corresponds to a currently running process. On newer
    Linux systems, will use the contents of ``/proc`` directory. For other
    systems, will use the output of ``ps -e``.

    :param pid: PID to check
    :type pid: int or string
    :rtype: Bool

.. py:function:: remove_pidfile(path)

    Remove PID file; doesn't complain about a file that doesn't exist, so you
    can call this as many times as you want.

.. py:function:: pidfile_is_stale(path)

    Checks if PID file already exists at ``path``, and if it is, whether the
    PID in the file refers to a stale (i.e. not running) process. Returns
    ``True`` if PID file exists and contains a not-running PID; otherwise
    returns ``False``.

    :rtype: Bool
    :raises: :py:class:`PIDFileError` if PID file exists and is malformed

.. py:function:: readpid(path)

    Reads PID from the file at ``path``.

    :rtype: string
    :raises: :py:class:`PIDFileError` if PID file is malformed

.. py:class:: PIDFileError

    PID file creation and parsing errors. Derived from ``Exception``.
