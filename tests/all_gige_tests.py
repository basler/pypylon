#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    # No priming discover(thisdir, pattern='nonexistent.py') call: see
    # all_emulated_tests.py for why that is unsafe.
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon', 'gigE'), pattern='*test.py'))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()