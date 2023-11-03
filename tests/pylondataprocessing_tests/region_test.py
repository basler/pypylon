from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class RegionTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.Region()
        self.assertFalse(testee1.IsValid())
        self.assertFalse(testee1.HasBoundingBox())
        self.assertFalse(testee1.HasReferenceSize())
        self.assertFalse(testee1.IsUnique())
        self.assertFalse(testee1.IsReadOnly())
        self.assertFalse(testee1.IsUserBufferAttached())
        self.assertEqual(testee1.GetBoundingBoxTopLeftX(), 0)
        self.assertEqual(testee1.GetBoundingBoxTopLeftY(), 0)
        self.assertEqual(testee1.GetBoundingBoxWidth(), 0)
        self.assertEqual(testee1.GetBoundingBoxHeight(), 0)
        self.assertEqual(testee1.GetReferenceWidth(), 0)
        self.assertEqual(testee1.GetReferenceHeight(), 0)
        self.assertEqual(testee1.GetAllocatedBufferSize(), 0)
        self.assertEqual(testee1.GetDataSize(), 0)
        self.assertEqual(testee1.GetRegionType(), pylondataprocessing.RegionType_Undefined)
        testee1.Release()
  
        #CRegion(ERegionType regionType,
        #        size_t dataSize,
        #        uint32_t referenceWidth = 0,
        #        uint32_t referenceHeight = 0,
        #        int32_t boundingBoxTopLeftX = 0,
        #        int32_t boundingBoxTopLeftY = 0,
        #        uint32_t boundingBoxWidth = 0,
        #        uint32_t boundingBoxHeight = 0);
        testee2 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 12, 100, 200, 10, 11, 12, 13)
        self.assertTrue(testee2.IsValid())
        self.assertTrue(testee2.HasBoundingBox())
        self.assertTrue(testee2.HasReferenceSize())
        self.assertTrue(testee2.IsUnique())
        self.assertFalse(testee2.IsReadOnly())
        self.assertFalse(testee2.IsUserBufferAttached())
        self.assertEqual(testee2.GetReferenceWidth(), 100)
        self.assertEqual(testee2.GetReferenceHeight(), 200)
        self.assertEqual(testee2.GetBoundingBoxTopLeftX(), 10)
        self.assertEqual(testee2.GetBoundingBoxTopLeftY(), 11)
        self.assertEqual(testee2.GetBoundingBoxWidth(), 12)
        self.assertEqual(testee2.GetBoundingBoxHeight(), 13)
        self.assertEqual(testee2.GetAllocatedBufferSize(), 12)
        self.assertEqual(testee2.GetDataSize(), 12)
        self.assertEqual(testee2.GetRegionType(), pylondataprocessing.RegionType_RLE32)
        self.assertEqual(testee2.ReferenceWidth, 100)
        self.assertEqual(testee2.ReferenceHeight, 200)
        self.assertEqual(testee2.BoundingBoxTopLeftX, 10)
        self.assertEqual(testee2.BoundingBoxTopLeftY, 11)
        self.assertEqual(testee2.BoundingBoxWidth, 12)
        self.assertEqual(testee2.BoundingBoxHeight, 13)
        self.assertEqual(testee2.AllocatedBufferSize, 12)
        self.assertEqual(testee2.DataSize, 12)
        self.assertEqual(testee2.RegionType, pylondataprocessing.RegionType_RLE32)
        testee3 = pylondataprocessing.Region(testee2)
        self.assertFalse(testee2.IsUnique())
        self.assertFalse(testee3.IsUnique())
        testee2.Release()
        self.assertFalse(testee2.IsValid())
        self.assertFalse(testee2.IsUnique())
        self.assertTrue(testee3.IsUnique())
        testee4 = pylondataprocessing.Region()
        testee4.CopyRegion(testee3) #deep copy
        self.assertTrue(testee4.IsValid())
        self.assertTrue(testee3.IsUnique())
        self.assertTrue(testee4.IsUnique())
        
    def test_rle32(self):
        testee1 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24, 100, 200, 10, 11, 12, 13)
        data = testee1.GetMemoryView() #no copy, direct access
        data4 = data.cast('i') # switch view to 4 byte integer
        data4[0] = 101
        data4[1] = 134
        data4[2] = 210

        data4[3] = 102
        data4[4] = 103
        data4[5] = 211
        data = None
        data4 = None
        
        dataArray = testee1.ToArray()
        self.assertEqual(dataArray[0].StartX, 101)
        self.assertEqual(dataArray[0].EndX, 134)
        self.assertEqual(dataArray[0].Y, 210)
        
        self.assertEqual(dataArray[1].StartX, 102)
        self.assertEqual(dataArray[1].EndX, 103)
        self.assertEqual(dataArray[1].Y, 211)
        testee1.Resize(36)
        self.assertEqual(testee1.GetDataSize(), 36)
        data = testee1.GetMemoryView()
        data4 = data.cast('i')
        data4[6] = 104
        data4[7] = 105
        data4[8] = 212
        dataArray = testee1.ToArray() #copies
        self.assertEqual(dataArray[0].StartX, 101)
        self.assertEqual(dataArray[0].EndX, 134)
        self.assertEqual(dataArray[0].Y, 210)
        
        self.assertEqual(dataArray[1].StartX, 102)
        self.assertEqual(dataArray[1].EndX, 103)
        self.assertEqual(dataArray[1].Y, 211)

        self.assertEqual(dataArray[2].StartX, 104)
        self.assertEqual(dataArray[2].EndX, 105)
        self.assertEqual(dataArray[2].Y, 212)
        
        byteArray = testee1.GetBuffer() #copies
        data4_2 = memoryview(byteArray).cast('i')

        self.assertEqual(data4_2[0], 101)
        self.assertEqual(data4_2[1], 134)
        self.assertEqual(data4_2[2], 210)
        self.assertEqual(data4_2[3], 102)
        self.assertEqual(data4_2[4], 103)
        self.assertEqual(data4_2[5], 211)
        self.assertEqual(data4_2[6], 104)
        self.assertEqual(data4_2[7], 105)
        self.assertEqual(data4_2[8], 212)

    def test_reset(self):
        testee1 = pylondataprocessing.Region(pylondataprocessing.RegionType_RLE32, 24, 100, 200, 10, 11, 12, 13)
        testee1.Reset(pylondataprocessing.RegionType_RLE32, 36, 101, 201, 20, 31, 42, 53)
        self.assertEqual(testee1.GetReferenceWidth(), 101)
        self.assertEqual(testee1.GetReferenceHeight(), 201)
        self.assertEqual(testee1.GetBoundingBoxTopLeftX(), 20)
        self.assertEqual(testee1.GetBoundingBoxTopLeftY(), 31)
        self.assertEqual(testee1.GetBoundingBoxWidth(), 42)
        self.assertEqual(testee1.GetBoundingBoxHeight(), 53)
        self.assertEqual(testee1.GetAllocatedBufferSize(), 36)
        self.assertEqual(testee1.GetDataSize(), 36)

if __name__ == "__main__":
    unittest.main()
