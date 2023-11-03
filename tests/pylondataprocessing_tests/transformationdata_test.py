from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class TransformationDataTestSuite(PylonDataProcessingTestCase):
    def checkAllZero(self, testee):
        for rowIndex in range(testee.RowCount):
            for columnIndex in range(testee.ColumnCount):
                self.assertEqual(testee.GetEntry(columnIndex, rowIndex), 0.0)

    def test_init(self):
        testee1 = pylondataprocessing.TransformationData()
        self.assertEqual(testee1.GetColumnCount(), 0)
        self.assertEqual(testee1.GetRowCount(), 0)
        self.assertEqual(testee1.ColumnCount, 0)
        self.assertEqual(testee1.RowCount, 0)
        self.assertEqual(testee1.IsValid(), False)
        testee2 = pylondataprocessing.TransformationData(3,2)
        self.assertEqual(testee2.GetColumnCount(), 3)
        self.assertEqual(testee2.GetRowCount(), 2)
        self.assertEqual(testee2.ColumnCount, 3)
        self.assertEqual(testee2.RowCount, 2)
        self.assertEqual(testee2.IsValid(), True)
        self.checkAllZero(testee2)

    def test_reset_and_set(self):
        testee = pylondataprocessing.TransformationData()
        testee.Reset(3,2)
        self.assertEqual(testee.GetColumnCount(), 3)
        self.assertEqual(testee.GetRowCount(), 2)
        self.assertEqual(testee.ColumnCount, 3)
        self.assertEqual(testee.RowCount, 2)
        self.assertEqual(testee.IsValid(), True)
        self.checkAllZero(testee)
        testee.SetEntry(0,0,1.2)
        self.assertEqual(testee.GetEntry(0, 0), 1.2)
        testee.Reset(4,3)
        self.assertEqual(testee.GetColumnCount(), 4)
        self.assertEqual(testee.GetRowCount(), 3)
        self.assertEqual(testee.ColumnCount, 4)
        self.assertEqual(testee.RowCount, 3)
        self.assertEqual(testee.IsValid(), True)
        self.checkAllZero(testee)
        testValue = 1.1
        for rowIndex in range(testee.RowCount):
            for columnIndex in range(testee.ColumnCount):
                testee.SetEntry(columnIndex, rowIndex, testValue)
                testValue += 1.0
        self.assertEqual(testValue, 13.1)
        testValue = 1.1
        for rowIndex in range(testee.RowCount):
            for columnIndex in range(testee.ColumnCount):
                self.assertEqual(testee.GetEntry(columnIndex, rowIndex), testValue)
                testValue += 1.0
        self.assertEqual(testValue, 13.1)



    def test_str(self):
        testee = pylondataprocessing.TransformationData(3,2)
        testValue = 1.1
        for rowIndex in range(testee.RowCount):
            for columnIndex in range(testee.ColumnCount):
                testee.SetEntry(columnIndex, rowIndex, testValue)
                testValue += 1.0
        self.assertEqual(testValue, 7.1)
        self.assertEqual(str(testee), "1.1, 2.1, 3.1\n4.1, 5.1, 6.1")

if __name__ == "__main__":
    unittest.main()
