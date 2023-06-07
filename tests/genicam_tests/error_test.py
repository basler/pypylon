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


class ErrorTestSuite(GenicamTestCase):
    def test_Basics(self):
        # added <pError> element
        # if(GenApiSchemaVersion == v1_0)
        #    return;

        """[ GenApiTest@ErrorTestSuite_TestBasics.xml|gxml
    
        <Integer Name="Value">
            <pError>Error</pError>
            <Value>42</Value>
        </Integer>
    
        <Enumeration Name="Error">
            <EnumEntry Name="NoError">
                <Value>0</Value>
           </EnumEntry>
            <EnumEntry Name="Ahrrgs">
                <ToolTip>A really awful error has happened</ToolTip>
                <Value>-1</Value>
           </EnumEntry>
            <Value>0</Value>
        </Enumeration>
    
        <Enumeration Name="EnumValue">
            <pError>Error</pError>
            <EnumEntry Name="Value0">
                <Value>0</Value>
           </EnumEntry>
            <EnumEntry Name="Value1">
                <Value>1</Value>
           </EnumEntry>
            <Value>0</Value>
        </Enumeration>
    
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ErrorTestSuite_TestBasics")

        Value = Camera.GetNode("Value")
        self.assertTrue(bool(Value))

        Error = Camera.GetNode("Error")
        self.assertTrue(bool(Error))

        EnumValue = Camera.GetNode("EnumValue")
        self.assertTrue(bool(EnumValue))

        # No error
        Value.SetValue(17)

        # error
        Error.SetValue("Ahrrgs")
        with self.assertRaises(RuntimeException):
            Value.SetValue(17)
        with self.assertRaises(RuntimeException):
            EnumValue.SetIntValue(1)

        # error suppressed
        Value.SetValue(17, False)
        EnumValue.SetIntValue(1, False)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
