#!/usr/bin/env python3
"""
Module MAIN
Sub-Package TEST.DBTOOLS of Package PLIB3
Copyright (C) 2008-2020 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This is the test-running script for the PLIB3.DBTOOLS test suite.
"""


if __name__ == '__main__':
    from plib.test.support import run_tests
    
    run_tests(__name__)
