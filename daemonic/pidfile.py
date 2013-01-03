# Copyright 2013 by Eric Suh
# This code is freely licensed under the MIT license found at
# <http://opensource.org/licenses/MIT>

import os
import subprocess
import errno
from contextlib import contextmanager

class PIDFileError(Exception):
    pass

@contextmanager
def pidfile(path, pid):
    make_pidfile(path, pid)
    yield
    remove_pidfile(path)

def readpid(path):
    with open(path) as f:
        pid = f.read().strip()
    if not pid.isdigit():
        raise PIDFileError('Malformed PID file at path {}'.format(path))
    return pid

def pidfile_is_stale(path):
    '''Checks if a PID file already exists there, and if it is, whether it
    is stale. Returns True if a PID file exists containing a PID for a
    process that does not exist any longer.'''
    try:
        pid = readpid(path)
    except IOError as e:
        if e.errno == errno.ENOENT:
            return False # nonexistant file isn't stale
        raise e
    if pid == '' or not pid.isdigit():
        raise PIDFileError('Malformed PID file at path {}'.format(path))
    return not is_pid_running(pid)

def _ps():
    raw = subprocess.check_output(['ps', '-eo', 'pid'])
    return [line.strip() for line in raw.split('\n')[1:] if line != '']

def is_pid_running(pid):
    try:
        procs = os.listdir('/proc')
    except OSError as e:
        if e.errno == errno.ENOENT:
            return str(pid) in _ps()
        raise e
    return str(pid) in [proc for proc in procs if proc.isdigit()]

def make_pidfile(path, pid):
    '''Create a PID file. '''
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    except OSError as e:
        if e.errno == errno.EEXIST:
            if pidfile_is_stale(path):
                remove_pidfile(path)
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
            else:
                raise PIDFileError(
                    'Non-stale PID file already exists at {}'.format(path))

    pidf = os.fdopen(fd, 'w')
    pidf.write(str(pid))
    pidf.flush()
    pidf.close()

def remove_pidfile(path):
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
