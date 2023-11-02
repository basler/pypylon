from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class EllipseFTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.EllipseF()
        self.assertEqual(testee1.Center.X, 0.0)
        self.assertEqual(testee1.Center.Y, 0.0)
        self.assertEqual(testee1.Radius1, 0.0)
        self.assertEqual(testee1.Radius2, 0.0)
        self.assertEqual(testee1.Rotation, 0.0)
        testee2 = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(testee2.Center.X, 1.2)
        self.assertEqual(testee2.Center.Y, 3.4)
        self.assertEqual(testee2.Radius1, 5.6)
        self.assertEqual(testee2.Radius2, 7.8)
        self.assertEqual(testee2.Rotation, 9.0)
        testee3 = pylondataprocessing.EllipseF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82, 9.02)
        self.assertEqual(testee3.Center.X, 1.22)
        self.assertEqual(testee3.Center.Y, 3.42)
        self.assertEqual(testee3.Radius1, 5.62)
        self.assertEqual(testee3.Radius2, 7.82)
        self.assertEqual(testee3.Rotation, 9.02)
        testee4 = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(testee4.Center.X, 1.2)
        self.assertEqual(testee4.Center.Y, 3.4)
        self.assertEqual(testee4.Radius1, 5.6)
        self.assertEqual(testee4.Radius2, 7.8)
        self.assertEqual(testee4.Rotation, 0.0)
        testee5 = pylondataprocessing.EllipseF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82)
        self.assertEqual(testee5.Center.X, 1.22)
        self.assertEqual(testee5.Center.Y, 3.42)
        self.assertEqual(testee5.Radius1, 5.62)
        self.assertEqual(testee5.Radius2, 7.82)
        self.assertEqual(testee5.Rotation, 0.0)
        testee6 = pylondataprocessing.EllipseF(testee5)
        self.assertEqual(testee6.Center.X, 1.22)
        self.assertEqual(testee6.Center.Y, 3.42)
        self.assertEqual(testee6.Radius1, 5.62)
        self.assertEqual(testee6.Radius2, 7.82)
        self.assertEqual(testee6.Rotation, 0.0)
        #Center returns _Center with a reference to its parent added
        #_Center holds a pointer to the C++ member SEllipseF::Center
        #EllipseF must not be released while using _Center
        self.assertEqual(testee6.Center.X, testee6._Center.X)
        testee6.Center.Y = 1234.5
        self.assertEqual(testee6.Center.Y, 1234.5)
        
    def test_str(self):
        testee = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(str(testee), "Center: (X = 1.2; Y = 3.4); Radius1 = 5.6; Radius2 = 7.8; Rotation = 9.0 rad")

if __name__ == "__main__":
    unittest.main()
