#!/usr/bin/env python
import unittest
import os

def load_tests(loader, tests, pattern):
    thisdir = os.path.dirname(__file__)
    suites = []
    # Pass top_level_dir=thisdir explicitly to every discover() call. This is
    # important for two reasons:
    #
    # 1. unittest.defaultTestLoader is a shared singleton that remembers the
    #    top_level_dir of the first discover() call and reuses it for later
    #    calls when top_level_dir is left as None. Without an explicit value the
    #    second call (pylon/emulated) would inherit the first call's
    #    top_level_dir (tests/genicam) and fail with
    #    "AssertionError: Path must be within the project".
    #
    # 2. Using the tests/ root as the common top level yields distinct, dotted
    #    module names (genicam.error_test vs pylondataprocessing.error_test), so
    #    same-named test modules in different suites (error_test.py exists in
    #    both tests/genicam and tests/pylondataprocessing) do not shadow each
    #    other in sys.modules.
    #
    # Each discover() still only imports the packages along its own start_dir,
    # so this does not walk the whole tests/ tree (e.g. it does not import
    # pylondataprocessing for the pure emulated suites).
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'genicam'), pattern='*test.py', top_level_dir=thisdir))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylon', 'emulated'), pattern='*test.py', top_level_dir=thisdir))
    suites.append(unittest.defaultTestLoader.discover( os.path.join(thisdir, 'pylondataprocessing'), pattern='*test.py', top_level_dir=thisdir))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main()