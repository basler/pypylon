import unittest
import os
import sys

#We want to keep the genicam tests the same as the ones in the genicam repository.
#So we can't change the code, but must work around its limitations.
#We add the directory to the path to be able to do:
# from genicamtestcase import GenicamTestCase
#and to fake
# from genicam import *
sys.path.insert(0, os.path.dirname(__file__))
