from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class CircleFTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.CircleF()
        self.assertEqual(testee1.Center.X, 0.0)
        self.assertEqual(testee1.Center.Y, 0.0)
        self.assertEqual(testee1.Radius, 0.0)
        testee2 = pylondataprocessing.CircleF(1.2, 3.4, 5.6)
        self.assertEqual(testee2.Center.X, 1.2)
        self.assertEqual(testee2.Center.Y, 3.4)
        self.assertEqual(testee2.Radius, 5.6)
        testee3 = pylondataprocessing.CircleF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62)
        self.assertEqual(testee3.Center.X, 1.22)
        self.assertEqual(testee3.Center.Y, 3.42)
        self.assertEqual(testee3.Radius, 5.62)
        testee4 = pylondataprocessing.CircleF(testee3)
        self.assertEqual(testee4.Center.X, 1.22)
        self.assertEqual(testee4.Center.Y, 3.42)
        self.assertEqual(testee4.Radius, 5.62)
        #Center returns _Center with a reference to its parent added
        #_Center holds a pointer to the C++ member SCircleF::Center
        #CircleF must not be released while using _Center
        self.assertEqual(testee4.Center.X, testee4._Center.X)
        testee4.Center.Y = 1234.5
        self.assertEqual(testee4.Center.Y, 1234.5)

    def test_str(self):
        testee = pylondataprocessing.CircleF(1.2, 3.4, 5.6)
        self.assertEqual(str(testee), "Center: (X = 1.2; Y = 3.4); Radius = 5.6")

if __name__ == "__main__":
    unittest.main()
