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


class PropertiesTestSuite(GenicamTestCase):
    def _find(self, List, String):
        found = False

        for e in List:
            if e == String:
                found = True
                break

        return found

    def test_PropertyAccess(self):
        # The nodes were not being loaded properly from the cache. 
        # Clearing the cache loads the nodes from the XML, eliminating the error.
        CNodeMapRef._ClearXMLCache()
        """[ GenApiTest@PropertiesTestSuite_TestPropertyAccess.xml|gxml
    
        <Category Name="Root">
            <pFeature>Register</pFeature>
            <pFeature>RegisterWithpLength</pFeature>
        </Category>
    
        <IntReg Name="Register">
            <pIsImplemented>Implemented</pIsImplemented>
            <pAddress>BaseAddress</pAddress>
            <pAddress>AddressOffset</pAddress>
            <Address>0x0100</Address>
            <Address>0x0e00</Address>
            <IntSwissKnife Name="Dummy">
                <pVariable Name="I">Index</pVariable>
                <Formula>0x0080 * I</Formula>
            </IntSwissKnife>
            <pIndex>Index</pIndex>
            <pIndex Offset="0x0080">Index</pIndex>
            <pIndex pOffset="IndexOffset">Index</pIndex>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>WriteThrough</Cachable>
            <pInvalidator>Invalidated</pInvalidator>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
            <pSelected>Changer</pSelected>
        </IntReg>
    
        <IntReg Name="RegisterWithpLength">
          <Address>0x0100</Address>
          <pLength>RegisterLength</pLength>
          <AccessMode>RW</AccessMode>
          <pPort>Port</pPort>
          <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0x2000</Value>
        </Integer>
    
        <Integer Name="AddressOffset">
            <Value>0xd000</Value>
        </Integer>
    
        <Integer Name="Index">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="IndexOffset">
          <Value>0</Value>
        </Integer>
    
        <Integer Name="Changer">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="Selector">
            <Value>0</Value>
            <pSelected>Register</pSelected>
        </Integer>
    
        <Integer Name="Implemented">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="Invalidated">
            <Value>1</Value>
        </Integer>
      
        <Integer Name="RegisterLength">
            <Value>1</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef("TestCamera")
        Camera._LoadXMLFromFile("GenApiTest", "PropertiesTestSuite_TestPropertyAccess")

        print("Dumping PropertyNames:\n")
        Nodes = Camera._GetNodes()
        for Node in Nodes:
            print("Node '", Node.Node.GetName(), "'\n")

            PropertyNames = Node.Node.GetPropertyNames()

            for Prop in PropertyNames:
                try:
                    ValueStr, AttributeStr = Node.Node.GetProperty(Prop)
                except LogicalErrorException:
                    print("\t  Property '", Prop, "' is not available\n")

                if AttributeStr == "":
                    print("\t  Property '", Prop, "' = '", ValueStr, "'\n")
                else:
                    print("\t  Property '", Prop, "' = '", ValueStr, "' [", AttributeStr, "]\n")

        Register = Camera.GetNode("Register")
        PropertyNames = Register.Node.GetPropertyNames()

        """
        AccessMode
        Address
        Cachable
        DeviceName
        Endianess
        ExposeStatic
        ImposedAccessMode
        IsDeprecated
        IsFeature
        Length
        Name
        NameSpace
        Representation
        Sign
        Streamable
        Visibility
        pAddress
        pDependent
        pIndex
        pInvalidator
        pIsImplemented
        pPort
        pSelected
        pSelecting
        pTerminal
        """
        self.assertEqual(0x1a, len(PropertyNames))

        self.assertTrue(self._find(PropertyNames, "AccessMode"))
        self.assertTrue(self._find(PropertyNames, "Address"))
        self.assertTrue(self._find(PropertyNames, "Cachable"))
        self.assertTrue(self._find(PropertyNames, "DeviceName"))
        self.assertTrue(self._find(PropertyNames, "Endianess"))
        self.assertTrue(self._find(PropertyNames, "ExposeStatic"))
        self.assertTrue(self._find(PropertyNames, "ImposedAccessMode"))
        self.assertTrue(self._find(PropertyNames, "IsDeprecated"))
        self.assertTrue(self._find(PropertyNames, "IsFeature"))
        self.assertTrue(self._find(PropertyNames, "Length"))
        self.assertTrue(self._find(PropertyNames, "Name"))
        self.assertTrue(self._find(PropertyNames, "NameSpace"))
        self.assertTrue(self._find(PropertyNames, "Representation"))
        self.assertTrue(self._find(PropertyNames, "Sign"))
        self.assertTrue(self._find(PropertyNames, "Streamable"))
        self.assertTrue(self._find(PropertyNames, "Visibility"))

        self.assertTrue(self._find(PropertyNames, "pAddress"))
        self.assertTrue(self._find(PropertyNames, "pDependent"))
        self.assertTrue(self._find(PropertyNames, "pIndex"))
        self.assertTrue(self._find(PropertyNames, "pInvalidator"))
        self.assertTrue(self._find(PropertyNames, "pIsImplemented"))
        self.assertTrue(self._find(PropertyNames, "pPort"))
        self.assertTrue(self._find(PropertyNames, "pDependent"))
        self.assertTrue(self._find(PropertyNames, "pSelected"))
        self.assertTrue(self._find(PropertyNames, "pSelecting"))
        self.assertTrue(self._find(PropertyNames, "pTerminal"))

        ValueStr = ""
        AttributeStr = ""
        ValueStr, AttributeStr = Register.Node.GetProperty("AccessMode")
        self.assertEqual("RW", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Address")
        self.assertEqual("256\t3584", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Cachable")
        self.assertEqual("WriteThrough", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("DeviceName")
        self.assertEqual("TestCamera", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Endianess")
        self.assertEqual("LittleEndian", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("ExposeStatic")
        self.assertEqual("Yes", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("ImposedAccessMode")
        self.assertEqual("RW", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("IsDeprecated")
        self.assertEqual("No", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("IsFeature")
        self.assertEqual("Yes", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Length")
        self.assertEqual("4", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Name")
        self.assertEqual("Register", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("NameSpace")
        self.assertEqual("Custom", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("NodeType")
        self.assertEqual("IntReg", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pAddress")
        # the number is generated by the pre-processor and subject to change
        self.assertEqual("BaseAddress\tAddressOffset\t", ValueStr[0:26])

        ValueStr, AttributeStr = Register.Node.GetProperty("pDependent")
        self.assertEqual("Changer\tRoot", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pIndex")
        self.assertEqual("Index\tIndex\tIndex", ValueStr)
        # the number is generated by the pre-processor and subject to change
        self.assertEqual("4\t128\tIndexOffset", AttributeStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pIsImplemented")
        self.assertEqual("Implemented", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pInvalidator")
        self.assertEqual("Invalidated", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pPort")
        self.assertEqual("Port", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pSelected")
        self.assertEqual("Changer", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pSelecting")
        self.assertEqual("Selector", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("Sign")
        self.assertEqual("Unsigned", ValueStr)

        ValueStr, AttributeStr = Register.Node.GetProperty("pTerminal")
        self.assertEqual("Register", ValueStr)

    def test_SwissKnifePropertyAccess(self):
        # The nodes were not being loaded properly from the cache. 
        # Clearing the cache loads the nodes from the XML, eliminating the error.
        CNodeMapRef._ClearXMLCache()
        """[ GenApiTest@PropertiesTestSuite_TestSwissKnifePropertyAccess.xml|gxml
    
        <IntSwissKnife Name="Result">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <Formula> X * Y + 12 </Formula>
        </IntSwissKnife>
    
        <Integer Name="ValueX">
            <Value>3</Value>
        </Integer>
    
        <Integer Name="ValueY">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PropertiesTestSuite_TestSwissKnifePropertyAccess")

        Result = Camera.GetNode("Result")

        PropertyNames = Result.Node.GetPropertyNames()

        print("Dumping PropertyNames:\n")
        for Prop in PropertyNames:
            try:
                ValueStr, AttributeStr = Result.Node.GetProperty(Prop)
            except LogicalErrorException:
                print("\tProperty '", Prop, "' is not available\n")

            if AttributeStr == "":
                print("\tProperty '", Prop, "' = '", ValueStr, "'\n")
            else:
                print("\tProperty '", Prop, "' = '", ValueStr, "' [", AttributeStr, "]\n")

        """
        Property 'DeviceName' = 'Device'
        Property 'ExposeStatic' = 'Yes'
        Property 'Formula' = ' X * Y + 12 '
        Property 'ImposedAccessMode' = 'RW'
        Property 'InputDirection' = 'None'
        Property 'IsDeprecated' = 'No'
        Property 'IsFeature' = 'No'
        Property 'Name' = 'Result'
        Property 'NameSpace' = 'Custom'
        Property 'NodeType' = 'IntSwissKnife'
        Property 'Representation' = 'PureNumber'
        Property 'Streamable' = 'No'
        Property 'Visibility' = 'Beginner'
        Property 'pVariable' = 'ValueX  ValueY' [X      Y]    """

        self.assertTrue(self._find(PropertyNames, "DeviceName"))
        self.assertTrue(self._find(PropertyNames, "ExposeStatic"))
        self.assertTrue(self._find(PropertyNames, "Formula"))
        self.assertTrue(self._find(PropertyNames, "ImposedAccessMode"))
        self.assertTrue(self._find(PropertyNames, "InputDirection"))
        self.assertTrue(self._find(PropertyNames, "IsDeprecated"))
        self.assertTrue(self._find(PropertyNames, "IsFeature"))
        self.assertTrue(self._find(PropertyNames, "Name"))
        self.assertTrue(self._find(PropertyNames, "NameSpace"))
        self.assertTrue(self._find(PropertyNames, "NodeType"))
        self.assertTrue(self._find(PropertyNames, "Representation"))
        self.assertTrue(self._find(PropertyNames, "Streamable"))
        self.assertTrue(self._find(PropertyNames, "Visibility"))
        self.assertTrue(self._find(PropertyNames, "pVariable"))

        self.assertEqual(14, len(PropertyNames))

        ValueStr, AttributeStr = Result.Node.GetProperty("Name")
        self.assertEqual("Result", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("NameSpace")
        self.assertEqual("Custom", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("NodeType")
        self.assertEqual("IntSwissKnife", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("DeviceName")
        self.assertEqual("Device", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("ExposeStatic")
        self.assertEqual("Yes", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("ImposedAccessMode")
        self.assertEqual("RW", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("InputDirection")
        self.assertEqual("None", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("IsDeprecated")
        self.assertEqual("No", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("IsFeature")
        self.assertEqual("No", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("Streamable")
        self.assertEqual("No", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("Representation")
        self.assertEqual("PureNumber", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("Visibility")
        self.assertEqual("Beginner", ValueStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("pVariable")
        self.assertEqual("ValueX\tValueY", ValueStr)
        self.assertEqual("X\tY", AttributeStr)

        ValueStr, AttributeStr = Result.Node.GetProperty("Formula")
        self.assertEqual(" X * Y + 12 ", ValueStr)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
