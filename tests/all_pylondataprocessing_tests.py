#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suite = unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylondataprocessing_tests'), pattern='*test.py')
    return suite

if __name__ == "__main__":
    unittest.main()