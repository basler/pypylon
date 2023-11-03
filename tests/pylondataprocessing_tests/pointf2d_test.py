from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class PointF2DTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.PointF2D()
        self.assertEqual(testee1.X, 0.0)
        self.assertEqual(testee1.Y, 0.0)
        testee2 = pylondataprocessing.PointF2D(1.2, 3.4)
        self.assertEqual(testee2.X, 1.2)
        self.assertEqual(testee2.Y, 3.4)
        testee3 = pylondataprocessing.PointF2D(testee2)
        self.assertEqual(testee3.X, 1.2)
        self.assertEqual(testee3.Y, 3.4)
        
    def test_str(self):
        testee = pylondataprocessing.PointF2D(1.2, 3.4)
        self.assertEqual(str(testee), "X = 1.2; Y = 3.4")

if __name__ == "__main__":
    unittest.main()
