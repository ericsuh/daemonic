# Copyright 2013 by Eric Suh
# This code is freely licensed under the MIT license found at
# <http://opensource.org/licenses/MIT>

import unittest
import test_pidfile

def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(
        test_pidfile.TestPIDFileFunctions)
    return suite
