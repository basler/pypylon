from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class RectangleFTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.RectangleF()
        self.assertEqual(testee1.Center.X, 0.0)
        self.assertEqual(testee1.Center.Y, 0.0)
        self.assertEqual(testee1.Width, 0.0)
        self.assertEqual(testee1.Height, 0.0)
        self.assertEqual(testee1.Rotation, 0.0)
        testee2 = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(testee2.Center.X, 1.2)
        self.assertEqual(testee2.Center.Y, 3.4)
        self.assertEqual(testee2.Width, 5.6)
        self.assertEqual(testee2.Height, 7.8)
        self.assertEqual(testee2.Rotation, 9.0)
        testee3 = pylondataprocessing.RectangleF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82, 9.02)
        self.assertEqual(testee3.Center.X, 1.22)
        self.assertEqual(testee3.Center.Y, 3.42)
        self.assertEqual(testee3.Width, 5.62)
        self.assertEqual(testee3.Height, 7.82)
        self.assertEqual(testee3.Rotation, 9.02)
        testee4 = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(testee4.Center.X, 1.2)
        self.assertEqual(testee4.Center.Y, 3.4)
        self.assertEqual(testee4.Width, 5.6)
        self.assertEqual(testee4.Height, 7.8)
        self.assertEqual(testee4.Rotation, 0.0)
        testee5 = pylondataprocessing.RectangleF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82)
        self.assertEqual(testee5.Center.X, 1.22)
        self.assertEqual(testee5.Center.Y, 3.42)
        self.assertEqual(testee5.Width, 5.62)
        self.assertEqual(testee5.Height, 7.82)
        self.assertEqual(testee5.Rotation, 0.0)
        testee6 = pylondataprocessing.RectangleF(testee5)
        self.assertEqual(testee6.Center.X, 1.22)
        self.assertEqual(testee6.Center.Y, 3.42)
        self.assertEqual(testee6.Width, 5.62)
        self.assertEqual(testee6.Height, 7.82)
        self.assertEqual(testee6.Rotation, 0.0)
        #Center returns _Center with a reference to its parent added
        #_Center holds a pointer to the C++ member SRectangleF::Center
        #RectangleF must not be released while using _Center
        self.assertEqual(testee6.Center.X, testee6._Center.X)
        testee6.Center.Y = 1234.5
        self.assertEqual(testee6.Center.Y, 1234.5)
        

    def test_str(self):
        testee = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(str(testee), "Center: (X = 1.2; Y = 3.4); Width = 5.6; Height = 7.8; Rotation = 9.0 rad")

if __name__ == "__main__":
    unittest.main()
