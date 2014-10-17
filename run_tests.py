#!/usr/bin/env python2

import sys
import unittest

from tests.func_tests import FunctionalTests


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(FunctionalTests),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())