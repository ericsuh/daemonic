# Copyright 2013 by Eric Suh
# This code is freely licensed under the MIT license found at
# <http://opensource.org/licenses/MIT>

import sys
import os
import errno
import atexit
import signal
import time

import pidfile

class daemon(object):
    'Context manager for POSIX daemon processes'

    def __init__(self,
                 pidfile=None,
                 workingdir='/',
                 umask=0,
                 stdin=None,
                 stdout=None,
                 stderr=None,
                ):
        self.pidfile = pidfile
        self.workingdir = workingdir
        self.umask = umask

        devnull = os.open(os.devnull, os.O_RDWR)
        if stdin is not None:  self.stdin = stdin.fileno()
        else:                  self.stdin = devnull
        if stdout is not None: self.stdout = stdout.fileno()
        else:                  self.stdout = devnull
        if stderr is not None: self.stderr = stderr.fileno()
        else:                  self.stderr = self.stdout
        os.close(devnull)

    def __enter__(self):
        self.daemonize()
        return

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()
        return

    def daemonize(self):
        '''Set up a daemon.

        There are a few major steps:
        1. Changing to a working directory that won't go away
        2. Changing user permissions mask
        3. Forking twice to detach from terminal and become new process leader
        4. Redirecting standard input/output
        5. Creating a PID file'''

        # Set up process conditions
        os.chdir(self.workingdir)
        os.umask(self.umask)

        # Double fork to daemonize
        _getchildfork(1)
        os.setsid()
        _getchildfork(2)

        # Redirect standard input/output files
        sys.stdin.flush()
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(stdin, sys.stdin.fileno())
        os.dup2(stdout, sys.stdout.fileno())
        os.dup2(stderr, sys.stderr.fileno())

        # Create PID file
        if self.pidfile is not None:
            pid = str(os.getpid())
            try:
                pidfile.make_pidfile(self.pidfile, pid)
            except PIDFileError as e:
                sys.stederr.write('Creating PID file failed. ({})'.format(e))
                os._exit(os.EX_OSERR)
        atexit.register(self.stop)

    def stop(self):
        if self.pidfile is not None:
            pid = pidfile.readpid(self.pidfile)
            try:
                while True:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)
            except OSError as e:
                if e.errno == errno.ESRCH:
                    pidfile.remove_pidfile(self.pidfile)
                else:
                    raise

def _getchildfork(n):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(os.EX_OK) # Exit in parent
    except OSError as e:
        sys.stederr.write('Fork #{} failed: {} ({})\n'.format(
            n, e.errno, e.strerror))
        os._exit(os.EX_OSERR)
