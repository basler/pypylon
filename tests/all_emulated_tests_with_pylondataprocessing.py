#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir), pattern='nonexistent.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'genicam_tests'), pattern='*test.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon_tests', 'emulated'), pattern='*test.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylondataprocessing_tests'), pattern='*test.py'))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()