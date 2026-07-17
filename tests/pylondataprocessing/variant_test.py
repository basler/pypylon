"""\
This unit test checks the Variant type bindings of pylondataprocessing.

It covers construction from each supported data type, conversion helpers,
array and sub-value access, error handling and the string representation.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
from pypylon import genicam
import unittest


class VariantTestSuite(PylonDataProcessingTestCase):

    def get_image_test_value_1(self):
        """Return a Mono8 test image of size 101x201."""
        result = pylon.PylonImage()
        result.Reset(pylon.PixelType_Mono8, 101, 201)
        return result

    def get_image_test_value_2(self):
        """Return a Mono8 test image of size 102x202."""
        result = pylon.PylonImage()
        result.Reset(pylon.PixelType_Mono8, 102, 202)
        return result

    # ------------------------------------------------------------------
    # Construction / factory
    # ------------------------------------------------------------------

    def test_init(self):
        """A default Variant has no data type and no values."""
        testee = pylondataprocessing.Variant()
        self.assertFalse(testee.IsArray())
        self.assertEqual(testee.GetDataType(), pylondataprocessing.VariantDataType_None)
        self.assertEqual(testee.DataType, pylondataprocessing.VariantDataType_None)
        self.assertEqual(testee.GetNumSubValues(), 0)
        self.assertEqual(testee.NumSubValues, 0)
        self.assertEqual(testee.GetNumArrayValues(), 0)
        self.assertEqual(testee.NumArrayValues, 0)

    def test_make_variant(self):
        """MakeVariant creates scalar and array variants and rejects unsupported containers."""
        scalar = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(scalar.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertFalse(scalar.IsArray())
        scalar_none_container = pylondataprocessing.Variant.MakeVariant(
            pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_None)
        self.assertEqual(scalar_none_container.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertFalse(scalar_none_container.IsArray())
        array = pylondataprocessing.Variant.MakeVariant(
            pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Array)
        self.assertEqual(array.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertTrue(array.IsArray())
        with self.assertRaises(genicam.InvalidArgumentException):
            pylondataprocessing.Variant.MakeVariant(
                pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Unsupported)
        with self.assertRaises(genicam.InvalidArgumentException):
            pylondataprocessing.Variant.MakeVariant(
                pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_None, 10)
        sized_array = pylondataprocessing.Variant.MakeVariant(
            pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Array, 10)
        self.assertEqual(sized_array.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertTrue(sized_array.IsArray())
        self.assertEqual(sized_array.GetNumArrayValues(), 10)
        with self.assertRaises(genicam.InvalidArgumentException):
            pylondataprocessing.Variant.MakeVariant(
                pylondataprocessing.VariantDataType_Int64, pylondataprocessing.VariantContainerType_Unsupported, 10)

    # ------------------------------------------------------------------
    # Scalar data types
    # ------------------------------------------------------------------

    def test_int64(self):
        """Variant round-trips Int64 values, copies and arrays."""
        test_value_1 = -100
        test_value_2 = -200
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee1.ToInt64(), test_value_1)
        self.assertEqual(testee1.ToData(), test_value_1)
        testee1.FromInt64(test_value_2)
        self.assertEqual(testee1.ToInt64(), test_value_2)
        self.assertEqual(testee1.ToData(), test_value_2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee4.FromInt64(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Int64)
        self.assertEqual(testee4.ToInt64(), test_value_1)
        self.assertEqual(testee4.ToData(), test_value_1)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0], test_value_1)
        self.assertEqual(as_array[1], test_value_2)

    def test_uint64(self):
        """Variant round-trips UInt64 values, copies and arrays."""
        test_value_1 = 100
        test_value_2 = 200
        # The Variant(testvalue) constructor is shadowed by Int64_t, so use MakeVariant as a workaround.
        testee1 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee1.FromUInt64(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_UInt64)
        self.assertEqual(testee1.ToUInt64(), test_value_1)
        self.assertEqual(testee1.ToData(), test_value_1)
        testee1.FromUInt64(test_value_2)
        self.assertEqual(testee1.ToUInt64(), test_value_2)
        self.assertEqual(testee1.ToData(), test_value_2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee4.FromUInt64(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_UInt64)
        self.assertEqual(testee4.ToUInt64(), test_value_1)
        self.assertEqual(testee4.ToData(), test_value_1)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        testee5 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee5.FromUInt64(test_value_2)
        array_variant.SetArrayItemValue(0, testee4)
        array_variant.SetArrayItemValue(1, testee5)
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0], test_value_1)
        self.assertEqual(as_array[1], test_value_2)

    def test_boolean(self):
        """Variant round-trips Boolean values, copies and arrays."""
        test_value_1 = True
        test_value_2 = False
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee1.ToBool(), test_value_1)
        self.assertEqual(testee1.ToData(), test_value_1)
        testee1.FromBool(test_value_2)
        self.assertEqual(testee1.ToBool(), test_value_2)
        self.assertEqual(testee1.ToData(), test_value_2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Boolean)
        testee4.FromBool(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(testee4.ToBool(), test_value_1)
        self.assertEqual(testee4.ToData(), test_value_1)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0], test_value_1)
        self.assertEqual(as_array[1], test_value_2)

    def test_string(self):
        """Variant round-trips String values, copies and arrays."""
        test_value_1 = "testvalue1"
        test_value_2 = "testvalue2"
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_String)
        self.assertEqual(testee1.ToString(), test_value_1)
        self.assertEqual(testee1.ToData(), test_value_1)
        testee1.FromString(test_value_2)
        self.assertEqual(testee1.ToString(), test_value_2)
        self.assertEqual(testee1.ToData(), test_value_2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_String)
        testee4.FromString(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_String)
        self.assertEqual(testee4.ToString(), test_value_1)
        self.assertEqual(testee4.ToData(), test_value_1)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0], test_value_1)
        self.assertEqual(as_array[1], test_value_2)

    def test_float(self):
        """Variant round-trips Float values, copies and arrays."""
        test_value_1 = 1.2
        test_value_2 = 2.3
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Float)
        self.assertEqual(testee1.ToDouble(), test_value_1)
        self.assertEqual(testee1.ToData(), test_value_1)
        testee1.FromDouble(test_value_2)
        self.assertEqual(testee1.ToDouble(), test_value_2)
        self.assertEqual(testee1.ToData(), test_value_2)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Float)
        testee4.FromDouble(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Float)
        self.assertEqual(testee4.ToDouble(), test_value_1)
        self.assertEqual(testee4.ToData(), test_value_1)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0], test_value_1)
        self.assertEqual(as_array[1], test_value_2)

    # ------------------------------------------------------------------
    # Complex data types
    # ------------------------------------------------------------------

    def test_pylon_image(self):
        """Variant round-trips PylonImage values, copies and arrays."""
        test_value_1 = self.get_image_test_value_1()
        test_value_2 = self.get_image_test_value_2()
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_PylonImage)
        self.assertEqual(testee1.ToImage().GetHeight(), test_value_1.GetHeight())
        self.assertEqual(testee1.ToData().GetHeight(), test_value_1.GetHeight())
        testee1.FromImage(test_value_2)
        self.assertEqual(testee1.ToImage().GetHeight(), test_value_2.GetHeight())
        self.assertEqual(testee1.ToData().GetHeight(), test_value_2.GetHeight())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_PylonImage)
        testee4.FromImage(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_PylonImage)
        self.assertEqual(testee4.ToImage().GetHeight(), test_value_1.GetHeight())
        self.assertEqual(testee4.ToData().GetHeight(), test_value_1.GetHeight())
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0].GetHeight(), test_value_1.GetHeight())
        self.assertEqual(as_array[1].GetHeight(), test_value_2.GetHeight())

    def test_region(self):
        """Variant round-trips Region values, copies and arrays."""
        test_value_1 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12)
        test_value_2 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24)
        # Known issues:
        # - when added to a variant, ReferenceHeight and bounding box info is stripped.
        # - the current version folds entries depending on buffer content; fill it to be deterministic.
        data = test_value_2.GetMemoryView()  # no copy, direct access
        data_as_int32 = data.cast('i')  # switch view to 4 byte integer
        data_as_int32[0] = 101
        data_as_int32[1] = 134
        data_as_int32[2] = 210

        data_as_int32[3] = 102
        data_as_int32[4] = 103
        data_as_int32[5] = 211
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_Region)
        self.assertEqual(testee1.ToRegion().GetDataSize(), test_value_1.GetDataSize())
        self.assertEqual(testee1.ToData().GetDataSize(), test_value_1.GetDataSize())
        testee1.FromRegion(test_value_2)
        self.assertEqual(testee1.ToRegion().GetDataSize(), test_value_2.GetDataSize())
        self.assertEqual(testee1.ToData().GetDataSize(), test_value_2.GetDataSize())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Region)
        testee4.FromRegion(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_Region)
        self.assertEqual(testee4.ToRegion().GetDataSize(), test_value_1.GetDataSize())
        self.assertEqual(testee4.ToData().GetDataSize(), test_value_1.GetDataSize())
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(as_array[0].GetDataSize(), test_value_1.GetDataSize())
        self.assertEqual(as_array[1].GetDataSize(), test_value_2.GetDataSize())

    def test_transformation_data(self):
        """Variant round-trips TransformationData values, copies and arrays."""
        test_value_1 = pylondataprocessing.TransformationData(2, 3)
        test_value_2 = pylondataprocessing.TransformationData(4, 5)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_TransformationData)
        self.assertEqual(testee1.ToTransformationData().GetColumnCount(), test_value_1.GetColumnCount())
        self.assertEqual(testee1.ToData().GetColumnCount(), test_value_1.GetColumnCount())
        testee1.FromTransformationData(test_value_2)
        self.assertEqual(testee1.ToTransformationData().GetColumnCount(), test_value_2.GetColumnCount())
        self.assertEqual(testee1.ToData().GetColumnCount(), test_value_2.GetColumnCount())
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_TransformationData)
        testee4.FromTransformationData(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_TransformationData)
        self.assertEqual(testee4.ToTransformationData().GetColumnCount(), test_value_1.GetColumnCount())
        self.assertEqual(testee4.ToData().GetColumnCount(), test_value_1.GetColumnCount())
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    def test_point_f2d(self):
        """Variant round-trips PointF2D values, copies and arrays."""
        test_value_1 = pylondataprocessing.PointF2D(1.2, 2.3)
        test_value_2 = pylondataprocessing.PointF2D(1.22, 2.32)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_PointF2D)
        self.assertEqual(testee1.ToPointF2D().X, test_value_1.X)
        self.assertEqual(testee1.ToData().X, test_value_1.X)
        testee1.FromPointF2D(test_value_2)
        self.assertEqual(testee1.ToPointF2D().X, test_value_2.X)
        self.assertEqual(testee1.ToData().X, test_value_2.X)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_PointF2D)
        testee4.FromPointF2D(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_PointF2D)
        self.assertEqual(testee4.ToPointF2D().X, test_value_1.X)
        self.assertEqual(testee4.ToData().X, test_value_1.X)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    def test_line_f2d(self):
        """Variant round-trips LineF2D values, copies and arrays."""
        test_value_1 = pylondataprocessing.LineF2D(1.2, 2.3, 4.5, 5.6)
        test_value_2 = pylondataprocessing.LineF2D(1.22, 2.32, 4.52, 5.62)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_LineF2D)
        self.assertEqual(testee1.ToLineF2D().PointA.X, test_value_1.PointA.X)
        self.assertEqual(testee1.ToData().PointA.X, test_value_1.PointA.X)
        testee1.FromLineF2D(test_value_2)
        self.assertEqual(testee1.ToLineF2D().PointA.X, test_value_2.PointA.X)
        self.assertEqual(testee1.ToData().PointA.X, test_value_2.PointA.X)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_LineF2D)
        testee4.FromLineF2D(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_LineF2D)
        self.assertEqual(testee4.ToLineF2D().PointA.X, test_value_1.PointA.X)
        self.assertEqual(testee4.ToData().PointA.X, test_value_1.PointA.X)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    def test_rectangle_f(self):
        """Variant round-trips RectangleF values, copies and arrays."""
        test_value_1 = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        test_value_2 = pylondataprocessing.RectangleF(1.22, 3.42, 5.62, 7.82, 9.02)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_RectangleF)
        self.assertEqual(testee1.ToRectangleF().Rotation, test_value_1.Rotation)
        self.assertEqual(testee1.ToData().Rotation, test_value_1.Rotation)
        testee1.FromRectangleF(test_value_2)
        self.assertEqual(testee1.ToRectangleF().Rotation, test_value_2.Rotation)
        self.assertEqual(testee1.ToData().Rotation, test_value_2.Rotation)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_RectangleF)
        testee4.FromRectangleF(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_RectangleF)
        self.assertEqual(testee4.ToRectangleF().Rotation, test_value_1.Rotation)
        self.assertEqual(testee4.ToData().Rotation, test_value_1.Rotation)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    def test_circle_f(self):
        """Variant round-trips CircleF values, copies and arrays."""
        test_value_1 = pylondataprocessing.CircleF(1.2, 2.3, 4.5)
        test_value_2 = pylondataprocessing.CircleF(1.22, 2.32, 4.52)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_CircleF)
        self.assertEqual(testee1.ToCircleF().Radius, test_value_1.Radius)
        self.assertEqual(testee1.ToData().Radius, test_value_1.Radius)
        testee1.FromCircleF(test_value_2)
        self.assertEqual(testee1.ToCircleF().Radius, test_value_2.Radius)
        self.assertEqual(testee1.ToData().Radius, test_value_2.Radius)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_CircleF)
        testee4.FromCircleF(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_CircleF)
        self.assertEqual(testee4.ToCircleF().Radius, test_value_1.Radius)
        self.assertEqual(testee4.ToData().Radius, test_value_1.Radius)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    def test_ellipse_f(self):
        """Variant round-trips EllipseF values, copies and arrays."""
        test_value_1 = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        test_value_2 = pylondataprocessing.EllipseF(1.22, 3.42, 5.62, 7.82, 9.02)
        testee1 = pylondataprocessing.Variant(test_value_1)
        self.assertEqual(testee1.GetDataType(), pylondataprocessing.VariantDataType_EllipseF)
        self.assertEqual(testee1.ToEllipseF().Rotation, test_value_1.Rotation)
        self.assertEqual(testee1.ToData().Rotation, test_value_1.Rotation)
        testee1.FromEllipseF(test_value_2)
        self.assertEqual(testee1.ToEllipseF().Rotation, test_value_2.Rotation)
        self.assertEqual(testee1.ToData().Rotation, test_value_2.Rotation)
        testee2 = testee1.Copy()
        testee3 = pylondataprocessing.Variant(testee1)
        self.assertFalse(testee1.IsEqualInstance(testee2))
        self.assertTrue(testee1.IsEqualInstance(testee3))
        testee4 = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_EllipseF)
        testee4.FromEllipseF(test_value_1)
        self.assertEqual(testee4.GetDataType(), pylondataprocessing.VariantDataType_EllipseF)
        self.assertEqual(testee4.ToEllipseF().Rotation, test_value_1.Rotation)
        self.assertEqual(testee4.ToData().Rotation, test_value_1.Rotation)
        array_variant = pylondataprocessing.Variant.MakeVariant(
            testee1.GetDataType(), pylondataprocessing.VariantContainerType_Array, 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(test_value_1))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(test_value_2))
        as_array = array_variant.ToData()
        self.assertEqual(len(as_array), 2)
        self.assertEqual(str(as_array[0]), str(test_value_1))
        self.assertEqual(str(as_array[1]), str(test_value_2))

    # ------------------------------------------------------------------
    # Comparison / errors / containers
    # ------------------------------------------------------------------

    def test_equals_operator(self):
        """The == operator compares variant instances by reference."""
        # Same-object referenced semantics.
        testee1 = pylondataprocessing.Variant("A")
        testee2 = pylondataprocessing.Variant(testee1)
        testee3 = pylondataprocessing.Variant("A")
        self.assertTrue(testee1 == testee2)
        self.assertFalse(testee1 == testee3)

    def test_data_error(self):
        """SetError marks a variant as erroneous and exposes the message."""
        testee = pylondataprocessing.Variant("A")
        self.assertFalse(testee.HasError())
        testee.SetError("Error message")
        self.assertTrue(testee.HasError())
        self.assertEqual(testee.GetErrorDescription(), "Error message")
        self.assertEqual(testee.ErrorDescription, "Error message")

    def test_get_error(self):
        """GetError returns an Error object describing the variant's error state."""
        if not hasattr(pylondataprocessing, "Error"):
            self.skipTest("Error is not available in this DataProcessing SDK version")
        testee = pylondataprocessing.Variant("A")
        testee.SetError("Error message")
        error = testee.GetError()
        self.assertIsInstance(error, pylondataprocessing.Error)
        self.assertTrue(error.IsValid())
        self.assertEqual(error.GetDescription(), "Error message")

    def test_set_error_from_error_object(self):
        """SetError accepts an Error object."""
        if not hasattr(pylondataprocessing, "Error"):
            self.skipTest("Error is not available in this DataProcessing SDK version")
        testee = pylondataprocessing.Variant("A")
        testee.SetError(pylondataprocessing.Error("Error message"))
        self.assertTrue(testee.HasError())
        self.assertEqual(testee.GetErrorDescription(), "Error message")

    def test_getitem_and_len(self):
        """Array variants support indexing, negative indices, len() and raise IndexError."""
        array_variant = pylondataprocessing.Variant.MakeVariant(
            pylondataprocessing.VariantDataType_Int64,
            pylondataprocessing.VariantContainerType_Array, 3,
        )
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(-10))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(-20))
        array_variant.SetArrayItemValue(2, pylondataprocessing.Variant(-30))

        self.assertEqual(len(array_variant), 3)
        self.assertEqual(array_variant[0].ToInt64(), -10)
        self.assertEqual(array_variant[1].ToInt64(), -20)
        self.assertEqual(array_variant[2].ToInt64(), -30)

        self.assertEqual(array_variant[-1].ToInt64(), -30)
        self.assertEqual(array_variant[-3].ToInt64(), -10)

        with self.assertRaises(IndexError):
            array_variant[3]
        with self.assertRaises(IndexError):
            array_variant[-4]

        scalar = pylondataprocessing.Variant("hello")
        self.assertEqual(len(scalar), 0)
        with self.assertRaises(IndexError):
            scalar[0]

    def test_convert(self):
        """CanConvert and Convert change the data type when possible."""
        non_convertible = pylondataprocessing.Variant("A")
        convertible = pylondataprocessing.Variant("1")
        self.assertFalse(non_convertible.CanConvert(pylondataprocessing.VariantDataType_Boolean))
        self.assertTrue(convertible.CanConvert(pylondataprocessing.VariantDataType_Boolean))
        converted = convertible.Convert(pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(converted.GetDataType(), pylondataprocessing.VariantDataType_Boolean)
        self.assertEqual(converted.ToBool(), True)

    def test_arrays(self):
        """Array variants can be resized and their items read back."""
        array_variant = pylondataprocessing.Variant.MakeVariant(
            pylondataprocessing.VariantDataType_Boolean, pylondataprocessing.VariantContainerType_Array, 5)
        self.assertTrue(array_variant.IsArray())
        self.assertEqual(array_variant.GetNumArrayValues(), 5)
        array_variant.ChangeArraySize(2)
        self.assertEqual(array_variant.GetNumArrayValues(), 2)
        array_variant.SetArrayItemValue(0, pylondataprocessing.Variant(False))
        array_variant.SetArrayItemValue(1, pylondataprocessing.Variant(True))
        self.assertEqual(array_variant.GetArrayValue(0).ToBool(), False)
        self.assertEqual(array_variant.GetArrayValue(1).ToBool(), True)
        as_array = array_variant.ToData()
        self.assertEqual(as_array[0], False)
        self.assertEqual(as_array[1], True)

    def test_subvalues(self):
        """Composite variants expose named sub-values."""
        testee = pylondataprocessing.Variant(pylondataprocessing.PointF2D(1.2, 2.3))
        self.assertEqual(testee.GetNumSubValues(), 2)
        self.assertEqual(testee.GetSubValueName(0), 'X')
        self.assertEqual(testee.GetSubValueName(1), 'Y')
        self.assertTrue(testee.HasSubValue('X'))
        self.assertFalse(testee.HasSubValue('Z'))
        testee.SetSubValue("X", pylondataprocessing.Variant(4.5))
        sub_value = testee.GetSubValue('X')
        self.assertEqual(sub_value.GetValueName(), 'X')
        self.assertEqual(testee.GetValueName("mypoint"), 'mypoint')  # root has no name, provide a default

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(Variant) renders the type, value and error state for every data type."""
        testee = pylondataprocessing.Variant()
        self.assertEqual(str(testee), "Type = None")
        testee = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee.FromInt64(-100)
        self.assertEqual(str(testee), "Type = Int64; -100")
        testee = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_UInt64)
        testee.FromUInt64(100)
        self.assertEqual(str(testee), "Type = UInt64; 100")
        testee = pylondataprocessing.Variant(True)
        self.assertEqual(str(testee), "Type = Boolean; true")
        testee = pylondataprocessing.Variant("testvalue1")
        self.assertEqual(str(testee), "Type = String; testvalue1")
        testee = pylondataprocessing.Variant(1.2)
        self.assertEqual(str(testee), "Type = Float; 1.2")
        testee = pylondataprocessing.Variant(self.get_image_test_value_1())
        self.assertEqual(str(testee), "Type = PylonImage")
        testee = pylondataprocessing.Variant(pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12))
        self.assertEqual(str(testee), "Type = Region")
        testee = pylondataprocessing.Variant(pylondataprocessing.TransformationData(2, 3))
        self.assertEqual(str(testee), "Type = TransformationData; 0.000, 0.000\n0.000, 0.000\n0.000, 0.000")
        testee = pylondataprocessing.Variant(pylondataprocessing.PointF2D(1.2, 2.3))
        self.assertEqual(str(testee), "Type = PointF2D; X = 1.2; Y = 2.3")
        testee = pylondataprocessing.Variant(pylondataprocessing.LineF2D(1.2, 2.3, 4.5, 5.6))
        self.assertEqual(str(testee), "Type = LineF2D; PointA: (X = 1.2; Y = 2.3); PointB: (X = 4.5; Y = 5.6)")
        testee = pylondataprocessing.Variant(pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0))
        self.assertEqual(str(testee), "Type = RectangleF; Center: (X = 1.2; Y = 3.4); Width = 5.6; Height = 7.8; Rotation = 9 rad")
        testee = pylondataprocessing.Variant(pylondataprocessing.CircleF(1.2, 2.3, 4.5))
        self.assertEqual(str(testee), "Type = CircleF; Center: (X = 1.2; Y = 2.3); Radius = 4.5")
        testee = pylondataprocessing.Variant(pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0))
        self.assertEqual(str(testee), "Type = EllipseF; Center: (X = 1.2; Y = 3.4); Radius1 = 5.6; Radius2 = 7.8; Rotation = 9 rad")

        testee = pylondataprocessing.Variant.MakeVariant(pylondataprocessing.VariantDataType_Int64)
        testee.FromInt64(-100)
        testee.SetError("Error Message")
        self.assertEqual(str(testee), "Type = Int64; Error = Error Message")


if __name__ == "__main__":
    unittest.main()
