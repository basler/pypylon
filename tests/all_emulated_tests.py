#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    # NOTE: do not discover(thisdir, ...) here, not even with a
    # non-matching pattern. unittest.discover() always imports every
    # __init__.py it recurses through (regardless of pattern), and both
    # tests/genicam/__init__.py and tests/pylon/emulated/__init__.py (as
    # well as tests/pylondataprocessing/__init__.py) do
    # sys.path.insert(0, <their own dir>) so same-named flat modules
    # (e.g. "from xxxtestcase import ...") resolve. Walking the whole
    # tests/ tree first would import tests/pylondataprocessing/__init__.py
    # too, putting it ahead on sys.path and shadowing same-named test
    # modules in other suites (e.g. error_test.py exists in both
    # tests/genicam and tests/pylondataprocessing) with the wrong one -
    # which fails to import on platforms without pylondataprocessing
    # (e.g. macOS). See AGENTS.md: "MacOS does not support
    # pylondataprocessing currently."
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'genicam'), pattern='*test.py'))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon', 'emulated'), pattern='*test.py'))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()