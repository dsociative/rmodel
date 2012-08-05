#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2
import sys

from teamcity.unittestpy import TeamcityTestRunner
from teamcity import underTeamcity

if __name__ == '__main__':

    count = 0
    errors = 0
    fails = 0

    if underTeamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest2.TextTestRunner()

    loader = unittest2.TestLoader()
    suites = loader.discover('./', pattern='zt_*.py')
    for suite in suites:
        result = runner.run(suite)
        errors += len(result.errors)
        fails += len(result.failures)
        count += suite.countTestCases()

    if errors or fails:
        sys.exit(1)
