# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:
#  $Header:
# -----------------------------------------------------------------------------

from genicam import *
import unittest
from genicamtestcase import GenicamTestCase


class CycleDetectorTestSuite(GenicamTestCase):
    def test_WriteCycles(self):
        """[ GenApiTest@CycleDetectorTestSuite_TestWriteCycles.xml|gxml
    
            <Integer Name = "ValueA">
                <pValue>ValueB</pValue>
            </Integer>
    
            <Integer Name = "ValueB">
                <pValue>ValueC</pValue>
            </Integer>
    
            <Integer Name = "ValueC">
                <pValueCopy>ValueB</pValueCopy>
                <pValue>ValueD</pValue>
            </Integer>
    
            <Integer Name = "ValueD">
                <Value>17</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        with self.assertRaises(RuntimeException):
            RuntimeException, Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestWriteCycles")

    def test_DependencyCycles(self):

        """[ GenApiTest@CycleDetectorTestSuite_TestDependencyCycles.xml|gxml
            
            <Integer Name="ValueA">
                <Value>17</Value>
                <pMax>ValueB</pMax>
            </Integer>
            <Integer Name="ValueB">
                <Value>17</Value>
                <pMax>ValueC</pMax>
            </Integer>
            <Integer Name="ValueC">
                <Value>17</Value>
                <pMin>ValueB</pMin>
                <pMax>ValueD</pMax>
            </Integer>
            <Integer Name="ValueD">
                <Value>17</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        with self.assertRaises(RuntimeException):
            Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestDependencyCycles")

    # Load check a file with a write cycle and a top level node
    def test_InfiniteRecursion(self):
        """[ GenApiTest@CycleDetectorTestSuite_TestInfiniteRecursion.xml|gxml
    
        <IntSwissKnife Name="WidthMax">
            <pVariable Name="OFFSET">OffsetValue</pVariable>
            <Formula>1000-OFFSET</Formula>
        </IntSwissKnife>
    
        <Integer Name="WidthValue">
            <Value>1000</Value>
            <pMax>WidthMax</pMax>
        </Integer>
    
        <IntSwissKnife Name="OffsetMax">
            <pVariable Name="WIDTH">WidthValue</pVariable>
            <Formula>1000-WIDTH</Formula>
        </IntSwissKnife>
    
        <Integer Name="OffsetValue">
            <Value>0</Value>
            <pMax>OffsetMax</pMax>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        if self.GenApiSchemaVersion == "v1_0":
            # {
            # for v1.0 schema the loader does not check for write cycles
            Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestInfiniteRecursion")

            # for backward compatibility this code must run. It works because there
            # are caches in the cycle

            WidthValue = Camera.GetNode("WidthValue")

            OffsetMax = Camera.GetNode("OffsetMax")

            self.assertEqual(1000, WidthValue.GetValue(True))
            self.assertEqual(0, OffsetMax.GetValue(True))
            WidthValue.SetValue(900)
            self.assertEqual(100, OffsetMax.GetValue(True))
        else:
            # for all other schema versions it does
            with self.assertRaises(RuntimeException):
                Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestInfiniteRecursion")

            # no nodes are created because of the cycle
            with self.assertRaises(AccessException):
                Camera.GetNode("WidthValue")
                # }

    # Mantis #89
    def test_Recursion(self):

        """[ GenApiTest@CycleDetectorTestSuite_TestRecursion.xml|gxml
    
        <IntSwissKnife Name="WidthMax">
            <pVariable Name="OFFSETX">OffsetXValue</pVariable>
            <Formula>1000-OFFSETX</Formula>
        </IntSwissKnife>
    
        <Integer Name="WidthValue">
            <Value>1000</Value>
            <pMax>WidthMax</pMax>
        </Integer>
    
        <IntSwissKnife Name="OffsetXMax">
            <pVariable Name="WIDTH">WidthValue</pVariable>
            <Formula>1000-WIDTH</Formula>
        </IntSwissKnife>
    
        <Integer Name="OffsetXValue">
            <Value>0</Value>
            <pMax>OffsetXMax</pMax>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        if self.GenApiSchemaVersion == "v1_0":
            # for v1.0 schema the loader does not check for write cycles
            Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestRecursion")

            # due ot backward compatibility the nodemap is created and the cycle is broken at runtime
            # using the caches
            Width = Camera.GetNode("WidthValue")

            WMax = Camera.GetNode("WidthMax")
            OffsetX = Camera.GetNode("OffsetXValue")
            OXMax = Camera.GetNode("OffsetXMax")

            Width.SetValue(500)
            OXMax.GetValue()
        else:
            # for all other schema versions it does
            with self.assertRaises(RuntimeException):
                Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestRecursion")

            # no nodes are created because of the cycle
            with self.assertRaises(AccessException):
                Camera.GetNode("WidthValue")

    def test_RecursionBreaker(self):
        """[ GenApiTest@CycleDetectorTestSuite_TestRecursionBreaker.xml|gxml
        
        <Category Name="Root">
            <pFeature>OuterSelector</pFeature>
            <pFeature>InnerSelector</pFeature>
            <pFeature>Feature</pFeature>
        </Category>
    
        <Integer Name="Feature">
            <Streamable>Yes</Streamable>
            <Value>192</Value>
            <Min>192</Min>
            <Max>1023</Max>
            <Representation>Linear</Representation>
            <!-- Recursion! -.
            <pSelected>OuterSelector</pSelected>
        </Integer>
    
        <Enumeration Name="InnerSelector">
            <EnumEntry Name="InnerEntry0" >
                <Value>0</Value>
            </EnumEntry>
            <Value>1</Value>
            <pSelected>Feature</pSelected>
        </Enumeration>
    
        <Enumeration Name="OuterSelector">
            <EnumEntry Name="OuterEntry0" >
                <Value>0</Value>
            </EnumEntry>
            <EnumEntry Name="OuterEntry1" >
                <Value>1</Value>
            </EnumEntry>
            <Value>1</Value>
            <pSelected>InnerSelector</pSelected>
        </Enumeration>
           
        """

        Camera = CNodeMapRef()
        with self.assertRaises(RuntimeException):
            Camera._LoadXMLFromFile("GenApiTest", "CycleDetectorTestSuite_TestRecursionBreaker")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
