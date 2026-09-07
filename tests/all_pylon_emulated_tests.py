#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    # No priming discover(thisdir, pattern='nonexistent.py') call: it still
    # imports every subpackage's __init__.py while recursing (regardless of
    # pattern), and those __init__.py files do sys.path.insert(0, <own dir>),
    # which can shadow same-named test modules discovered afterwards.
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon', 'emulated'), pattern='*test.py'))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()