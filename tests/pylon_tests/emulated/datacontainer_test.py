from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import unittest
import os


class DataContainerTestSuite(PylonEmuTestCase):

    def test_empty_container(self):
        testee = pylon.PylonDataContainer()
        self.assertEqual(testee.DataComponentCount, 0)
        self.assertEqual(testee.GetDataComponentCount(), 0)
        testee.Release()
        try:
            testee.GetDataComponent(0)
        except genicam.OutOfRangeException:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            testee.Save("dummyfilename")
        except genicam.LogicalErrorException:
            pass
        else:
            self.fail("Exception not raised.")
        #testee.Load(filename) //load is test below

    def test_empty_container_component(self):
        testee = pylon.PylonDataComponent()
        self.assertEqual(testee.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(testee.ComponentType, 0)
        self.assertEqual(testee.IsValid(), False)
        self.assertEqual(testee.Width, 0)
        self.assertEqual(testee.Height, 0)
        self.assertEqual(testee.OffsetX, 0)
        self.assertEqual(testee.OffsetY, 0)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.DataSize, 0)
        self.assertEqual(testee.TimeStamp, 0)
        self.assertEqual(testee.GetComponentType(), 0)
        self.assertEqual(testee.GetPixelType(), pylon.PixelType_Undefined)
        self.assertEqual(testee.GetWidth(), 0)
        self.assertEqual(testee.GetHeight(), 0)
        self.assertEqual(testee.GetOffsetX(), 0)
        self.assertEqual(testee.GetOffsetY(), 0)
        self.assertEqual(testee.GetPaddingX(), 0)
        self.assertEqual(testee.GetDataSize(), 0)
        self.assertEqual(testee.GetTimeStamp(), 0)
        testee.GetData()
    
    def test_container_load(self):
        testee1 = pylon.PylonDataContainer()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        testee1.Load(filename)
        self.assertEqual(testee1.DataComponentCount, 3)
        testee2 = testee1.GetDataComponent(0)
        self.assertEqual(testee2.IsValid(), True)
        self.assertEqual(testee2.PixelType, pylon.PixelType_Coord3D_ABC32f)
        self.assertEqual(testee2.ComponentType, pylon.ComponentType_Range)
        self.assertEqual(testee2.Width, 160)
        self.assertEqual(testee2.Height, 120)
        self.assertEqual(testee2.OffsetX, 80)
        self.assertEqual(testee2.OffsetY, 60)
        self.assertEqual(testee2.PaddingX, 0)
        self.assertEqual(testee2.DataSize, 230400)
        self.assertEqual(testee2.TimeStamp, 62653150103775)
        testee2.Array
        self.assertEqual(testee2.GetData()[0], 79)
        self.assertEqual(testee2.GetMemoryView()[0], 79)
        #self.assertEqual(testee2.Array[0,0], [-468.76804, -338.49225,  746.62396])
        testee3 = testee1.GetDataComponent(1)
        self.assertEqual(testee3.IsValid(), True)
        self.assertEqual(testee3.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(testee3.ComponentType, pylon.ComponentType_Intensity)
        self.assertEqual(testee3.Width, 160)
        self.assertEqual(testee3.Height, 120)
        self.assertEqual(testee3.OffsetX, 80)
        self.assertEqual(testee3.OffsetY, 60)
        self.assertEqual(testee3.PaddingX, 0)
        self.assertEqual(testee3.DataSize, 38400)
        self.assertEqual(testee3.TimeStamp, 62653150103775)
        self.assertEqual(testee3.Array[0,0], 20388)
        self.assertEqual(testee3.GetData()[0], 164)
        self.assertEqual(testee3.GetMemoryView()[0], 164)
        testee4 = testee1.GetDataComponent(2)
        self.assertEqual(testee4.IsValid(), True)
        self.assertEqual(testee4.PixelType, pylon.PixelType_Confidence16)
        self.assertEqual(testee4.ComponentType, pylon.ComponentType_Confidence)
        self.assertEqual(testee4.Width, 160)
        self.assertEqual(testee4.Height, 120)
        self.assertEqual(testee4.OffsetX, 80)
        self.assertEqual(testee4.OffsetY, 60)
        self.assertEqual(testee4.PaddingX, 0)
        self.assertEqual(testee4.DataSize, 38400)
        self.assertEqual(testee4.TimeStamp, 62653150103775)
        self.assertEqual(testee4.Array[0,0], 1769)
        self.assertEqual(testee4.GetData()[0], 233)
        self.assertEqual(testee4.GetMemoryView()[0], 233)
        testee4.Release()
        self.assertEqual(testee4.IsValid(), False)
        testee3.Release()
        testee2.Release()
        testee1.Release()

    def test_container_load_zero_copy(self):
        testee1 = pylon.PylonDataContainer()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        testee1.Load(filename)
        self.assertEqual(testee1.DataComponentCount, 3)
        testee3 = testee1.GetDataComponent(1)
        with testee3.GetArrayZeroCopy() as zc:
            self.assertEqual(zc[0,0], 20388)
        testee3.Release()
        testee1.Release()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
