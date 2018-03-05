import os
import sys

#adding this dir to the path allows:
# from pylonemutestcase import PylonEmuTestCase
#THis is no clean solution, but works for now
sys.path.insert(0, os.path.dirname(__file__))
