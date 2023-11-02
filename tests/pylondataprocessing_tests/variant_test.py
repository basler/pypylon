from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
from pypylon import genicam
import unittest

class VariantTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee = pylondataprocessing.Variant()
        self.assertFalse(testee.IsArray())
        self.assertEqual(testee.GetDataType(), pylondataprocessing.VariantDataType_None)
        self.assertEqual(testee.DataType, pylondataprocessing.VariantDataType_None)
        self.assertEqual(testee.GetNumSubValues(), 0)
        self.assertEqual(testee.NumSubValues, 0)
        self.assertEqual(testee.GetNumArrayValues(), 0)
        self.assertEqual(testee.NumArrayValues, 0)
        
    def getImageTestValue1(self):
        result = pylon.PylonImage()
        result.Reset(pylon.PixelType_Mono8, 101, 201)
        return result

    def getImageTestValue2(self):
        result = pylon.PylonImage()
        result.Reset(pylon.PixelType_Mono8, 102, 202)
        return result

    def test_MakeVariant(self):
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertFalse(testee1.IsArray())
        testee2 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_None)
        self.assertEqual(testee2.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertFalse(testee2.IsArray())
        testee3 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Array)
        self.assertEqual(testee3.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertTrue(testee3.IsArray())
        try:
            pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Unsupported)
        except genicam.InvalidArgumentException:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_None, 10)
        except genicam.InvalidArgumentException:
            pass
        else:
            self.fail("Exception not raised.")
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Array, 10)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertTrue(testee4.IsArray())
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee4.GetNumArrayValues(), 10)
        try:
            pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Unsupported, 10)
        except genicam.InvalidArgumentException:
            pass
        else:
            self.fail("Exception not raised.")

    def test_Int64(self):
        testvalue1 = -100
        testvalue2 = -200
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee1.ToInt64(), testvalue1)
        testee1.FromInt64(testvalue2)
        self.assertEqual(testee1.ToInt64(), testvalue2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee4.FromInt64(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee4.ToInt64(), testvalue1)

    def test_UInt64(self):
        testvalue1 = 100
        testvalue2 = 200
        #testee1 = pylondataprocessing.Variant(testvalue1) this constructor is shadowed by Int64_t
        #workaround
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee1.FromUInt64(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_UInt64)
        self.assertEqual(testee1.ToUInt64(), testvalue1)
        testee1.FromUInt64(testvalue2)
        self.assertEqual(testee1.ToUInt64(), testvalue2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee4.FromUInt64(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_UInt64)
        self.assertEqual(testee4.ToUInt64(), testvalue1)

    def test_Boolean(self):
        testvalue1 = True
        testvalue2 = False
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee1.ToBool(), testvalue1)
        testee1.FromBool(testvalue2)
        self.assertEqual(testee1.ToBool(), testvalue2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Boolean)
        testee4.FromBool(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee4.ToBool(), testvalue1)

    def test_String(self):
        testvalue1 = "testvalue1"
        testvalue2 = "testvalue2"
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_String)
        self.assertEqual(testee1.ToString(), testvalue1)
        testee1.FromString(testvalue2)
        self.assertEqual(testee1.ToString(), testvalue2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_String)
        testee4.FromString(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_String)
        self.assertEqual(testee4.ToString(), testvalue1)

    def test_Float(self):
        testvalue1 = 1.2
        testvalue2 = 2.3
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Float)
        self.assertEqual(testee1.ToDouble(), testvalue1)
        testee1.FromDouble(testvalue2)
        self.assertEqual(testee1.ToDouble(), testvalue2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Float)
        testee4.FromDouble(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Float)
        self.assertEqual(testee4.ToDouble(), testvalue1)

    def test_PylonImage(self):
        testvalue1 = self.getImageTestValue1()
        testvalue2 = self.getImageTestValue2()
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_PylonImage)
        self.assertEqual(testee1.ToImage().GetHeight(), testvalue1.GetHeight())
        testee1.FromImage(testvalue2)
        self.assertEqual(testee1.ToImage().GetHeight(), testvalue2.GetHeight())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_PylonImage)
        testee4.FromImage(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_PylonImage)
        self.assertEqual(testee4.ToImage().GetHeight(), testvalue1.GetHeight())

    def test_Region(self):
        testvalue1 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12)
        testvalue2 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24)
        #known issues
        #info: when added to a variant ReferenceHeight and BoundingBox info is stripped
        #start current version folds entries depending on buffer content, make deterministic
        data = testvalue2.GetMemoryView() #no copy, direct access
        data4 = data.cast('i') # switch view to 4 byte integer
        data4[0] = 101
        data4[1] = 134
        data4[2] = 210

        data4[3] = 102
        data4[4] = 103
        data4[5] = 211
        #end current version folds entries depending on buffer content
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Region)
        self.assertEqual(testee1.ToRegion().GetDataSize(), testvalue1.GetDataSize())
        testee1.FromRegion(testvalue2)
        self.assertEqual(testee1.ToRegion().GetDataSize(), testvalue2.GetDataSize())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Region)
        testee4.FromRegion(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Region)
        self.assertEqual(testee4.ToRegion().GetDataSize(), testvalue1.GetDataSize())

    def test_TransformationData(self):
        testvalue1 = pylondataprocessing.TransformationData(2, 3)
        testvalue2 = pylondataprocessing.TransformationData(4, 5)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_TransformationData)
        self.assertEqual(testee1.ToTransformationData().GetColumnCount(), testvalue1.GetColumnCount())
        testee1.FromTransformationData(testvalue2)
        self.assertEqual(testee1.ToTransformationData().GetColumnCount(), testvalue2.GetColumnCount())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_TransformationData)
        testee4.FromTransformationData(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_TransformationData)
        self.assertEqual(testee4.ToTransformationData().GetColumnCount(), testvalue1.GetColumnCount())

    def test_PointF2D(self):
        testvalue1 = pylondataprocessing.PointF2D(1.2, 2.3)
        testvalue2 = pylondataprocessing.PointF2D(1.22, 2.32)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_PointF2D)
        self.assertEqual(testee1.ToPointF2D().X, testvalue1.X)
        testee1.FromPointF2D(testvalue2)
        self.assertEqual(testee1.ToPointF2D().X, testvalue2.X)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_PointF2D)
        testee4.FromPointF2D(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_PointF2D)
        self.assertEqual(testee4.ToPointF2D().X, testvalue1.X)

    def test_LineF2D(self):
        testvalue1 = pylondataprocessing.LineF2D(1.2, 2.3, 4.5, 5.6)
        testvalue2 = pylondataprocessing.LineF2D(1.22, 2.32, 4.52, 5.62)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_LineF2D)
        self.assertEqual(testee1.ToLineF2D().PointA.X, testvalue1.PointA.X)
        testee1.FromLineF2D(testvalue2)
        self.assertEqual(testee1.ToLineF2D().PointA.X, testvalue2.PointA.X)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_LineF2D)
        testee4.FromLineF2D(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_LineF2D)
        self.assertEqual(testee4.ToLineF2D().PointA.X, testvalue1.PointA.X)

    def test_RectangleF(self):
        testvalue1 = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        testvalue2 = pylondataprocessing.RectangleF(1.22, 3.42, 5.62, 7.82, 9.02)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_RectangleF)
        self.assertEqual(testee1.ToRectangleF().Rotation, testvalue1.Rotation)
        testee1.FromRectangleF(testvalue2)
        self.assertEqual(testee1.ToRectangleF().Rotation, testvalue2.Rotation)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_RectangleF)
        testee4.FromRectangleF(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_RectangleF)
        self.assertEqual(testee4.ToRectangleF().Rotation, testvalue1.Rotation)

    def test_CircleF(self):
        testvalue1 = pylondataprocessing.CircleF(1.2, 2.3, 4.5)
        testvalue2 = pylondataprocessing.CircleF(1.22, 2.32, 4.52)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_CircleF)
        self.assertEqual(testee1.ToCircleF().Radius, testvalue1.Radius)
        testee1.FromCircleF(testvalue2)
        self.assertEqual(testee1.ToCircleF().Radius, testvalue2.Radius)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_CircleF)
        testee4.FromCircleF(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_CircleF)
        self.assertEqual(testee4.ToCircleF().Radius, testvalue1.Radius)

    def test_EllipseF(self):
        testvalue1 = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        testvalue2 = pylondataprocessing.EllipseF(1.22, 3.42, 5.62, 7.82, 9.02)
        testee1 = pylondataprocessing.Variant(testvalue1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_EllipseF)
        self.assertEqual(testee1.ToEllipseF().Rotation, testvalue1.Rotation)
        testee1.FromEllipseF(testvalue2)
        self.assertEqual(testee1.ToEllipseF().Rotation, testvalue2.Rotation)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_EllipseF)
        testee4.FromEllipseF(testvalue1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_EllipseF)
        self.assertEqual(testee4.ToEllipseF().Rotation, testvalue1.Rotation)

    def test_equalsOperator(self):
        #same object referenced semantics
        testee1 = pylondataprocessing.Variant("A")
        testee2 = pylondataprocessing.Variant(testee1)
        testee3 = pylondataprocessing.Variant("A")
        self.assertTrue(testee1 == testee2)
        self.assertFalse(testee1 == testee3)

    def test_dataError(self):
        testee1 = pylondataprocessing.Variant("A")
        self.assertFalse(testee1.HasError())
        testee1.SetError("Error message")
        self.assertTrue(testee1.HasError())
        self.assertEqual(testee1.GetErrorDescription(), "Error message")
        
    def test_convert(self):
        testee1 = pylondataprocessing.Variant("A")
        testee2 = pylondataprocessing.Variant("1")
        self.assertFalse(testee1.CanConvert(pylondataprocessing.VariantDataType_Boolean))
        self.assertTrue(testee2.CanConvert(pylondataprocessing.VariantDataType_Boolean))
        testee3 = testee2.Convert(pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee3.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee3.ToBool(), True)

    def test_arrays(self):
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Boolean, pylondataprocessing.VariantContainerType_Array, 5)
        self.assertTrue(testee1.IsArray())
        self.assertEqual(testee1.GetNumArrayValues(), 5)
        testee1.ChangeArraySize(2)
        self.assertEqual(testee1.GetNumArrayValues(), 2)
        testee1.SetArrayItemValue(0, pylondataprocessing.Variant(False))
        testee1.SetArrayItemValue(1, pylondataprocessing.Variant(True))
        self.assertEqual(testee1.GetArrayValue(0).ToBool(), False)
        self.assertEqual(testee1.GetArrayValue(1).ToBool(), True)

    def test_subvalues(self):
        testee1 = pylondataprocessing.Variant(pylondataprocessing.PointF2D(1.2, 2.3))
        self.assertEqual(testee1.GetNumSubValues(), 2)
        self.assertEqual(testee1.GetSubValueName(0), 'X')
        self.assertEqual(testee1.GetSubValueName(1), 'Y')
        self.assertTrue(testee1.HasSubValue('X'))
        self.assertFalse(testee1.HasSubValue('Z'))
        testee1.SetSubValue("X", pylondataprocessing.Variant(4.5))
        subvariant = testee1.GetSubValue('X')
        self.assertEqual(subvariant.GetValueName(), 'X')
        self.assertEqual(testee1.GetValueName("mypoint"), 'mypoint') #root has no name, provide a default

    def test_str(self):
        testee1 = pylondataprocessing.Variant()
        self.assertEqual(str(testee1), "Type = None")
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee1.FromInt64(-100)
        self.assertEqual(str(testee1), "Type = Int64; -100")
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee1.FromUInt64(100)
        self.assertEqual(str(testee1), "Type = UInt64; 100")
        testee1 = pylondataprocessing.Variant(True)
        self.assertEqual(str(testee1), "Type = Boolean; true")
        testee1 = pylondataprocessing.Variant("testvalue1")
        self.assertEqual(str(testee1), "Type = String; testvalue1")
        testee1 = pylondataprocessing.Variant(1.2)
        self.assertEqual(str(testee1), "Type = Float; 1.2")
        testee1 = pylondataprocessing.Variant(self.getImageTestValue1())
        self.assertEqual(str(testee1), "Type = PylonImage")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12))
        self.assertEqual(str(testee1), "Type = Region")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.TransformationData(2, 3))
        self.assertEqual(str(testee1), "Type = TransformationData; 0.000, 0.000\n0.000, 0.000\n0.000, 0.000")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.PointF2D(1.2, 2.3))
        self.assertEqual(str(testee1), "Type = PointF2D; X = 1.2; Y = 2.3")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.LineF2D(1.2, 2.3, 4.5, 5.6))
        self.assertEqual(str(testee1), "Type = LineF2D; PointA: (X = 1.2; Y = 2.3); PointB: (X = 4.5; Y = 5.6)")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0))
        self.assertEqual(str(testee1), "Type = RectangleF; Center: (X = 1.2; Y = 3.4); Width = 5.6; Height = 7.8; Rotation = 9 rad")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.CircleF(1.2, 2.3, 4.5))
        self.assertEqual(str(testee1), "Type = CircleF; Center: (X = 1.2; Y = 2.3); Radius = 4.5")
        testee1 = pylondataprocessing.Variant(pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0))
        self.assertEqual(str(testee1), "Type = EllipseF; Center: (X = 1.2; Y = 3.4); Radius1 = 5.6; Radius2 = 7.8; Rotation = 9 rad")

        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee1.FromInt64(-100)
        testee1.SetError("Error Message")
        self.assertEqual(str(testee1), "Type = Int64; Error = Error Message")

if __name__ == "__main__":
    unittest.main()
