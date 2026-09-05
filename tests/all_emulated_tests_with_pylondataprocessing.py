#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    # NOTE: no priming discover(thisdir, pattern='nonexistent.py') call here.
    # See all_emulated_tests.py for why that pattern is unsafe: it still
    # imports every subpackage __init__.py it recurses through, and each
    # test subpackage inserts its own directory at the front of sys.path,
    # which can shadow same-named test modules (e.g. error_test.py exists
    # in both tests/genicam and tests/pylondataprocessing) discovered later.
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'genicam'), pattern='*test.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon', 'emulated'), pattern='*test.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylondataprocessing'), pattern='*test.py'))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()