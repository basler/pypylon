from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class LineF2DTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.LineF2D()
        self.assertEqual(testee1.PointA.X, 0.0)
        self.assertEqual(testee1.PointA.Y, 0.0)
        self.assertEqual(testee1.PointB.X, 0.0)
        self.assertEqual(testee1.PointB.Y, 0.0)
        testee2 = pylondataprocessing.LineF2D(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(testee2.PointA.X, 1.2)
        self.assertEqual(testee2.PointA.Y, 3.4)
        self.assertEqual(testee2.PointB.X, 5.6)
        self.assertEqual(testee2.PointB.Y, 7.8)
        testee3 = pylondataprocessing.LineF2D(pylondataprocessing.PointF2D(1.22, 3.42), pylondataprocessing.PointF2D(5.62, 7.82))
        self.assertEqual(testee3.PointA.X, 1.22)
        self.assertEqual(testee3.PointA.Y, 3.42)
        self.assertEqual(testee3.PointB.X, 5.62)
        self.assertEqual(testee3.PointB.Y, 7.82)
        testee4 = pylondataprocessing.LineF2D(testee3)
        self.assertEqual(testee4.PointA.X, 1.22)
        self.assertEqual(testee4.PointA.Y, 3.42)
        self.assertEqual(testee4.PointB.X, 5.62)
        self.assertEqual(testee4.PointB.Y, 7.82)
        #PointA returns _PointA with a reference to its parent added
        #_PointA holds a pointer to the C++ member SLineF2D::PointA
        #LineF2D must not be released while using _PointA
        self.assertEqual(testee4.PointA.X, testee4._PointA.X) 
        self.assertEqual(testee4.PointB.X, testee4._PointB.X)
        testee4.PointB.Y = 1234.5
        self.assertEqual(testee4.PointB.Y, 1234.5)
        

    def test_str(self):
        testee = pylondataprocessing.LineF2D(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(str(testee), "PointA: (X = 1.2; Y = 3.4); PointB: (X = 5.6; Y = 7.8)")

if __name__ == "__main__":
    unittest.main()
