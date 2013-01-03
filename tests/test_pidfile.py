# Copyright 2013 by Eric Suh
# This code is freely licensed under the MIT license found at
# <http://opensource.org/licenses/MIT>

import os
import os.path
import sys
import tempfile
import subprocess
import errno
import unittest

sys.path.insert(0, '..')

from daemonic import pidfile

class TestPIDFileFunctions(unittest.TestCase):

    def setUp(self):
        self.path = '/tmp/pidfiles-test.pid'
        try:
            os.remove(self.path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        self.pid = subprocess.check_output('echo $$', shell=True).strip()
        self.currentpid = os.getpid()

    def tearDown(self):
        try:
            os.remove(self.path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise

    def test_is_pid_running(self):
        self.assertTrue(pidfile.is_pid_running(self.currentpid),
                        'Incorrectly identifying running state of PID')
        self.assertFalse(pidfile.is_pid_running(self.pid),
                        'Incorrectly identifying not running state of PID')

    def test_makeremove_pidfile(self):
        pidfile.make_pidfile(self.path, self.pid)
        self.assertTrue(os.path.exists(self.path), 'Creating PID file failed')

        with open(self.path) as f:
            x = f.read()
            self.assertEqual(x, str(self.pid), 'PID file contents incorrect')
        pidfile.remove_pidfile(self.path)

        self.assertFalse(os.path.exists(self.path), 'Removing PID file failed')

    def test_stale_pidfiles(self):
        pidfile.make_pidfile(self.path, self.pid)
        self.assertTrue(pidfile.pidfile_is_stale(self.path),
                       'Incorrectly stating PID file is not stale')
        # Since file is stale, safe to override
        pidfile.make_pidfile(self.path, self.currentpid)
        pidfile.remove_pidfile(self.path)

        pidfile.make_pidfile(self.path, self.currentpid)
        self.assertFalse(pidfile.pidfile_is_stale(self.path),
                         'Incorrectly stating PID file is stale')
        with self.assertRaises(pidfile.PIDFileError):
            # File exists and is not stale
            pidfile.make_pidfile(self.path, self.currentpid)
        pidfile.remove_pidfile(self.path)


if __name__ == '__main__':
    unittest.main()
