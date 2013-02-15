#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2
import sys

if __name__ == '__main__':

    count = 0
    errors = 0
    fails = 0

    runner = unittest2.TextTestRunner()

    loader = unittest2.TestLoader()
    suites = loader.discover('./', pattern='zt_*.py')
    result = runner.run(suites)
    errors += len(result.errors)
    fails += len(result.failures)
    count += suites.countTestCases()

    if errors or fails:
        sys.exit(1)
