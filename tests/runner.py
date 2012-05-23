#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

if __name__ == '__main__':

    MASK = 'Test'

    runner = unittest.TextTestRunner()
    loader = unittest.TestLoader()
    suites = loader.discover('./', pattern='zt_*.py')
    for suite in suites:
        runner.run(suite)
