from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class VariantDataTypeTestSuite(PylonDataProcessingTestCase):
    def test_presence(self):
        self.assertEqual(pylondataprocessing.VariantDataType_Int64, 1)             
        self.assertEqual(pylondataprocessing.VariantDataType_UInt64, 2)            
        self.assertEqual(pylondataprocessing.VariantDataType_Boolean, 3)           
        self.assertEqual(pylondataprocessing.VariantDataType_String, 4)            
        self.assertEqual(pylondataprocessing.VariantDataType_Float, 5)             
        self.assertEqual(pylondataprocessing.VariantDataType_PylonImage, 6)        
        self.assertEqual(pylondataprocessing.VariantDataType_Region, 8)            
        self.assertEqual(pylondataprocessing.VariantDataType_TransformationData, 9)
        self.assertEqual(pylondataprocessing.VariantDataType_Composite, 7)
        self.assertEqual(pylondataprocessing.VariantDataType_PointF2D, 10)
        self.assertEqual(pylondataprocessing.VariantDataType_LineF2D, 11)
        self.assertEqual(pylondataprocessing.VariantDataType_RectangleF, 12)
        self.assertEqual(pylondataprocessing.VariantDataType_CircleF, 13)
        self.assertEqual(pylondataprocessing.VariantDataType_EllipseF, 14)
        self.assertEqual(pylondataprocessing.VariantDataType_None, 0)

if __name__ == "__main__":
    unittest.main()
