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


class StreamingTestSuite(GenicamTestCase):
    def test_SimpleStreaming(self):
        """[ GenApiTest@StreamingTestSuite_TestSimpleStreaming.xml|gxml
    
        <Integer Name="Streaming">
            <Streamable>Yes</Streamable>
            <Value>20</Value>
        </Integer>
    
        <Integer Name="NoStreaming">
            <Streamable>No</Streamable>
            <Value>20</Value>
        </Integer>
    
        <Integer Name="SelectedA">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="SelectedAA">
            <pValue>SelectedA</pValue>
        </Integer>
    
        <Node Name="SelectedB"/>
    
        <Integer Name="Selector1">
            <Value>1</Value>
            <pSelected>SelectedA</pSelected>
            <pSelected>SelectedB</pSelected>
        </Integer>
    
        <Integer Name="Selector2">
            <Value>1</Value>
            <pSelected>SelectedA</pSelected>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StreamingTestSuite_TestSimpleStreaming")

        Streaming = Camera.GetNode("Streaming")

        NoStreaming = Camera.GetNode("NoStreaming")

        Selector1 = Camera.GetNode("Selector1")

        Selector2 = Camera.GetNode("Selector2")

        SelectedA = Camera.GetNode("SelectedA")

        SelectedAA = Camera.GetNode("SelectedAA")

        SelectedB = Camera.GetNode("SelectedB")

        """----- check the streaming flag ---"""
        self.assertEqual(True, Streaming.GetNode().IsStreamable())
        self.assertEqual(False, NoStreaming.GetNode().IsStreamable())

        """----- check the Selector list---"""
        self.assertEqual(True, Selector1.Node.IsSelector())
        self.assertEqual(True, Selector2.Node.IsSelector())
        self.assertEqual(False, SelectedA.Node.IsSelector())
        self.assertEqual(False, SelectedAA.Node.IsSelector())
        self.assertEqual(False, SelectedB.Node.IsSelector())

        SelectedFeatures = Selector1.Node.GetSelectedFeatures()
        self.assertEqual(3, len(SelectedFeatures))
        self.assertEqual("SelectedAA", SelectedFeatures[2].GetNode().GetName())
        self.assertEqual("SelectedB", SelectedFeatures[1].GetNode().GetName())
        self.assertEqual("SelectedA", SelectedFeatures[0].GetNode().GetName())

        SelectedFeatures = Selector2.Node.GetSelectedFeatures()
        self.assertEqual(2, len(SelectedFeatures))
        self.assertEqual("SelectedAA", SelectedFeatures[1].GetNode().GetName())
        self.assertEqual("SelectedA", SelectedFeatures[0].GetNode().GetName())

        SelectedFeatures = SelectedA.Node.GetSelectedFeatures()
        self.assertEqual(0, len(SelectedFeatures))

        SelectedFeatures = SelectedAA.Node.GetSelectedFeatures()
        self.assertEqual(0, len(SelectedFeatures))

        SelectedFeatures = SelectedB.Node.GetSelectedFeatures()
        self.assertEqual(0, len(SelectedFeatures))

        """----- check the Selecting list---"""

        SelectingFeatures = Selector1.Node.GetSelectingFeatures()
        self.assertEqual(0, len(SelectingFeatures))

        SelectingFeatures = Selector2.Node.GetSelectingFeatures()
        self.assertEqual(0, len(SelectingFeatures))

        SelectingFeatures = SelectedA.Node.GetSelectingFeatures()

        self.assertEqual(2, len(SelectingFeatures))
        self.assertEqual("Selector2", SelectingFeatures[1].GetNode().GetName())
        self.assertEqual("Selector1", SelectingFeatures[0].GetNode().GetName())

        SelectingFeatures = SelectedB.Node.GetSelectingFeatures()
        self.assertEqual(1, len(SelectingFeatures))
        self.assertEqual("Selector1", SelectingFeatures[0].GetNode().GetName())

        SelectingFeatures = SelectedAA.Node.GetSelectingFeatures()
        self.assertEqual(2, len(SelectingFeatures))
        self.assertEqual("Selector2", SelectingFeatures[1].GetNode().GetName())
        self.assertEqual("Selector1", SelectingFeatures[0].GetNode().GetName())

    def test_VeryTestSimpleStreaming(self):
        """[ GenApiTest@StreamingTestSuite_VeryTestSimpleStreaming.xml|gxml
    
        <Integer Name="SelectedA">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="SelectedAA">
            <pValue>SelectedA</pValue>
        </Integer>
    
        <Integer Name="Selector1">
            <Value>1</Value>
            <pSelected>SelectedA</pSelected>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StreamingTestSuite_VeryTestSimpleStreaming")

        Selector1 = Camera.GetNode("Selector1")

        SelectedA = Camera.GetNode("SelectedA")

        SelectedAA = Camera.GetNode("SelectedAA")

        SelectingFeatures = SelectedAA.Node.GetSelectingFeatures()
        i = 1
        self.assertEqual(i, len(SelectingFeatures))
        self.assertEqual("Selector1", SelectingFeatures[i - 1].GetNode().GetName())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
