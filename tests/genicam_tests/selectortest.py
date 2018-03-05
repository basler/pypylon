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
from testport import CTestPort


class cb(object):
    def __init__(self):
        self.m_Count = 0

    def doCount(self, Node):
        self.m_Count += 1

    def Count(self):
        return self.m_Count


class SelectorTestSuite(GenicamTestCase):
    # Test a selector of integer type
    def test_Selector01(self):
        """[ GenApiTest@SelectorTestSuite_TestSelector01.xml|gxml
          <Category Name="catUserSet">
            <ToolTip>the one and only category</ToolTip>
            <DisplayName>"A"</DisplayName>
            <Visibility>Beginner</Visibility>
            <pFeature>regUserSetName</pFeature>
            <pFeature>UserSetVersion</pFeature>
        </Category>
        <Integer Name="selector">
            <Extension/>
            <ToolTip>Integer is a selector for category a</ToolTip>
            <DisplayName>Mode</DisplayName>
            <Visibility>Beginner</Visibility>
            <Value>0</Value>
            <Min>0</Min>
            <Max>1</Max>
            <Inc>1</Inc>
            <Representation>Linear</Representation>
                <pSelected>catUserSet</pSelected>
        </Integer>
        <Float Name="UserSetVersion">
            <pValue>rVersion</pValue>
        </Float>
        <FloatReg Name="rVersion">
            <pAddress>adrCategory_A</pAddress>
            <Address>0x0</Address>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>myPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <StringReg Name="regUserSetName">
            <DisplayName>Name</DisplayName>
            <pAddress>adrCategory_A</pAddress>
            <Address>0x4</Address>
            <pLength>UserSetNameLen</pLength>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
        </StringReg>
      <Integer Name="UserSetNameLen">
       <Value>48</Value>
      </Integer>
        <IntSwissKnife Name="adrCategory_A">
            <Visibility>Invisible</Visibility>
            <pVariable Name="INDEX">selector</pVariable>
            <Formula>0x1000+0x100*INDEX</Formula>
        </IntSwissKnife>
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector01")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x2000, "uint32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(1, len(selected))
        Node01 = selected[0].GetNode()

        name01 = "catUserSet"
        self.assertEqual(name01, Node01.GetName())

    # Test a selector of enum type
    def test_Selector02(self):
        """[ GenApiTest@SelectorTestSuite_TestSelector02.xml|gxml
            <Category Name="catUserSet">
            <Extension/>
            <ToolTip>the one and only category</ToolTip>
            <DisplayName>A</DisplayName>
            <Visibility>Beginner</Visibility>
            <pFeature>regUserSetName</pFeature>
            <pFeature>UserSetVersion</pFeature>
        </Category>
        <Enumeration Name="selector">
            <EnumEntry Name="MySettings">
                <Value>0</Value>
            </EnumEntry>
            <EnumEntry Name="HansSettings">
                <Value>1</Value>
            </EnumEntry>
            <pValue>regSelector</pValue>
                <pSelected>catUserSet</pSelected>
                <pSelected>UserSetVersion</pSelected>
        </Enumeration>
        <IntReg Name="regSelector">
            <Address>0x0</Address>
            <Length>2</Length>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
        <Float Name="UserSetVersion">
            <pValue>rVersion</pValue>
        </Float>
        <FloatReg Name="rVersion">
            <pAddress>adrCategory_A</pAddress>
            <Address>0x0</Address>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>myPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <StringReg Name="regUserSetName">
            <DisplayName>Name</DisplayName>
            <pAddress>adrCategory_A</pAddress>
            <Address>0x4</Address>
            <pLength>UserSetNameLen</pLength>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
        </StringReg>
      <Integer Name="UserSetNameLen">
       <Value>48</Value>
      </Integer>
        <IntSwissKnife Name="adrCategory_A">
            <Visibility>Invisible</Visibility>
            <pVariable Name="INDEX">regSelector</pVariable>
            <Formula>0x1000+0x100*INDEX</Formula>
        </IntSwissKnife>
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector02")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x2000, "uint32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(2, len(selected))
        Node01 = selected[0].GetNode()
        Node02 = selected[1].GetNode()

        name01 = "catUserSet"
        name02 = "UserSetVersion"
        self.assertEqual(name01, Node01.GetName())
        self.assertEqual(name02, Node02.GetName())

    # Test selector of masked int reg type
    def test_Selector03(self):
        """[ GenApiTest@SelectorTestSuite_TestSelector03.xml|gxml
            <Category Name="catUserSet">
            <Extension/>
            <ToolTip>the one and only category</ToolTip>
            <DisplayName>A</DisplayName>
            <Visibility>Beginner</Visibility>
            <pFeature>regUserSetName</pFeature>
            <pFeature>UserSetVersion</pFeature>
        </Category>
        <MaskedIntReg Name="selector">
            <Address>0x0</Address>
            <Length>2</Length>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
            <Bit>4</Bit>
            <Endianess>LittleEndian</Endianess>
                <pSelected>catUserSet</pSelected>
                <pSelected>UserSetVersion</pSelected>
        </MaskedIntReg>
            <Float Name="UserSetVersion">
            <pValue>rVersion</pValue>
        </Float>
        <FloatReg Name="rVersion">
            <pAddress>adrCategory_A</pAddress>
            <Address>0x0</Address>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>myPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <StringReg Name="regUserSetName">
            <DisplayName>Name</DisplayName>
            <pAddress>adrCategory_A</pAddress>
            <Address>0x4</Address>
            <pLength>UserSetNameLen</pLength>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
        </StringReg>
      <Integer Name="UserSetNameLen">
       <Value>48</Value>
      </Integer>
        <IntSwissKnife Name="adrCategory_A">
            <Visibility>Invisible</Visibility>
            <pVariable Name="INDEX">selector</pVariable>
            <Formula>0x1000+0x100*INDEX</Formula>
        </IntSwissKnife>
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector03")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x2000, "uint32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(2, len(selected))
        Node01 = selected[0].GetNode()
        Node02 = selected[1].GetNode()

        name01 = "catUserSet"
        name02 = "UserSetVersion"
        self.assertEqual(name01, Node01.GetName())
        self.assertEqual(name02, Node02.GetName())

        c = cb()
        Register(Node01, c.doCount)
        Register(Node02, c.doCount)

        SelectorNode = Selector.GetNode()
        SelectorNode.InvalidateNode()

    # Test selector of int reg type
    def test_Selector04(self):
        """[ GenApiTest@SelectorTestSuite_TestSelector04.xml|gxml
            <Category Name="catUserSet">
            <Extension/>
            <ToolTip>the one and only category</ToolTip>
            <DisplayName>A</DisplayName>
            <Visibility>Beginner</Visibility>
            <pFeature>regUserSetName</pFeature>
            <pFeature>UserSetVersion</pFeature>
        </Category>
        <IntReg Name="selector">
            <Address>0x0</Address>
            <Length>3</Length>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
                <pSelected>regUserSetName</pSelected>
                <pSelected>UserSetVersion</pSelected>
        </IntReg>
        <Float Name="UserSetVersion">
            <pValue>rVersion</pValue>
        </Float>
        <FloatReg Name="rVersion">
            <pAddress>adrCategory_A</pAddress>
            <Address>0x0</Address>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>myPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <StringReg Name="regUserSetName">
            <DisplayName>Name</DisplayName>
            <pAddress>adrCategory_A</pAddress>
            <Address>0x4</Address>
            <pLength>UserSetNameLen</pLength>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
        </StringReg>
      <Integer Name="UserSetNameLen">
       <Value>48</Value>
      </Integer>
        <IntSwissKnife Name="adrCategory_A">
            <Visibility>Invisible</Visibility>
            <pVariable Name="INDEX">selector</pVariable>
            <Formula>0x1000+0x100*INDEX</Formula>
        </IntSwissKnife>
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector04")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x2000, "uint32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(2, len(selected))
        Node01 = selected[0].GetNode()
        Node02 = selected[1].GetNode()

        name01 = "regUserSetName"
        name02 = "UserSetVersion"
        self.assertEqual(name01, Node01.GetName())
        self.assertEqual(name02, Node02.GetName())

    # -------------------------------------------------------------
    """*
    *  \brief Test selector of an array
    *
    *  A minimal register description is created. The root category
    *  contains two features only. The selector is a "floating" integer
    *  node with range from 40 to 49. The integer register "entry" is
    *  one of the ten elements of the array. The index and the addres
    *  are directly determined by the selector.
    *
    *  The test iterates through the whole array and sets the value.
    *  The registered callback object c counts the invalidation calls.
    """

    def test_Selector05(self):
        """[ GenApiTest@SelectorTestSuite_TestSelector05.xml|gxml
    
      <Category Name="Root">
       <pFeature>Entry</pFeature>
       <pFeature>selector</pFeature>
      </Category>
    
        <IntReg Name="Entry">
       <pAddress>selector</pAddress>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
      <Integer Name="selector">
       <Value>48</Value>
       <Min>40</Min>
       <Max>49</Max>
       <pSelected>Entry</pSelected>
      </Integer>
    
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector05")

        # create and initialize a test port
        Port = CTestPort()
        for i in range(40, 50):
            Port.CreateEntry(i, "uint8_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(1, len(selected))
        Node01 = selected[0].GetNode()

        name01 = "Entry"
        self.assertEqual(name01, Node01.GetName())

        c = cb()
        Register(Node01, c.doCount)

        for i in range(Selector.GetMin(), Selector.GetMax() + 1, Selector.GetInc()):
            print(i)
            Selector.SetValue(i)
            # print(Value.ToString())

        self.assertEqual(10, c.Count())

    # -------------------------------------------------------------
    """*
    *  \brief Test selector of a catgory
    *
    *  A category must not become a selected item even if one of its features is selected
    """

    def test_Selector06(self):

        """[ GenApiTest@SelectorTestSuite_TestSelector06.xml|gxml
        <Category Name="ACategory">
            <pFeature>ASelectedFeature</pFeature>
            <pFeature>ASelector</pFeature>
        </Category>
        <Integer Name="ASelectedFeature">
            <Value>0</Value>
        </Integer>
        <Integer Name="ASelector">
            <Value>0</Value>
            <pSelected>ASelectedFeature</pSelected>
        </Integer>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector06")

        SelectedFeature = Camera.GetNode("ASelectedFeature")

        SelectingFeatures = SelectedFeature.Node.GetSelectingFeatures()
        self.assertEqual(1, len(SelectingFeatures))
        self.assertEqual(SelectingFeatures[0].GetNode().GetName(), "ASelector")

        Category = Camera.GetNode("ACategory")
        SelectingFeatures = Category.Node.GetSelectingFeatures()
        # nobody is selecting a category
        self.assertEqual(0, len(SelectingFeatures))

    """*
    *  \brief Test selector of a catgory
    *
    *  A dependencies must be unique
    """

    def test_Selector07(self):

        """[ GenApiTest@SelectorTestSuite_TestSelector07.xml|gxml
    
        <Integer Name="Integer">
            <pValue>Value</pValue>
            <pMin>Min</pMin>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="Min">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="Selector">
            <Value>0</Value>
            <pSelected>Value</pSelected>
            <pSelected>Min</pSelected>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelector07")

        Integer = Camera.GetNode("Integer")

        SelectingFeatures = Integer.Node.GetSelectingFeatures()
        self.assertEqual(1, len(SelectingFeatures))
        self.assertEqual(SelectingFeatures[0].GetNode().GetName(), "Selector")

        Integer = Camera.GetNode("Min")

        SelectingFeatures = Integer.Node.GetSelectingFeatures()
        self.assertEqual(1, len(SelectingFeatures))
        self.assertEqual(SelectingFeatures[0].GetNode().GetName(), "Selector")

        Integer = Camera.GetNode("Value")

        SelectingFeatures = Integer.Node.GetSelectingFeatures()
        self.assertEqual(1, len(SelectingFeatures))
        self.assertEqual(SelectingFeatures[0].GetNode().GetName(), "Selector")

        Integer = Camera.GetNode("Selector")

        SelectingFeatures = Integer.Node.GetSelectingFeatures()
        self.assertEqual(0, len(SelectingFeatures))

    def test_BracketOperator(self):

        # TODO : implement bracket operator
        # This a new experimental feature that needs to be/ can be further elaborated.
        # if 0

        # using namespace Test_TestCamera_v1_1
        # CTestCamera_v1_1 Camera
        # Camera._LoadDLL()

        # Camera.Gain[ GainSelector_Green ].SetValue( 42 )
        # self.assertEqual( (int64_t) 42LL, dynamic_cast<IInteger*>(Camera.GetNode("GainGreen")).GetValue() )
        # self.assertEqual( gcstring("Green"), Camera.GainSelector.ToString() )
        # Camera.Gain[ GainSelector_Green ].SetValue( 815 )
        # self.assertEqual( (int64_t) 815LL, dynamic_cast<IInteger*>(Camera.GetNode("GainGreen")).GetValue() )

        # Camera.Gain[ GainSelector_Red ].SetValue( 42 )
        # self.assertEqual( (int64_t) 42LL, dynamic_cast<IInteger*>(Camera.GetNode("GainRed")).GetValue() )
        # self.assertEqual( gcstring("Red"), Camera.GainSelector.ToString() )
        # Camera.Gain[ GainSelector_Red ].SetValue( 815 )
        # self.assertEqual( (int64_t) 815LL, dynamic_cast<IInteger*>(Camera.GetNode("GainRed")).GetValue() )

        # Camera.Gain[ GainMode_Analog ].SetValue( 42 )
        # Camera.Gain[ GainSelector_Green ][ GainMode_Analog ].SetValue( 42 )

        # Camera.Gain[ GainMode_Digital ][ GainSelector_Blue ].SetValue( 12345 )
        # self.assertEqual( (int64_t) 12345LL, dynamic_cast<IInteger*>(Camera.GetNode("GainBlue")).GetValue() )
        # self.assertEqual( gcstring("Blue"), Camera.GainSelector.ToString() )
        # self.assertEqual( gcstring("Digital"), Camera.GainMode.ToString() )

        # Camera.Gain.SetSelector( GainSelector_Green ).SetSelector( GainMode_Analog ).SetSelector( 3 ).SetValue( 42 )
        # Camera.Gain[ GainSelector_Green ][ GainMode_Analog ][3] = 42
        # endif
        pass

    def test_BooleanSelector(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@SelectorTestSuite_TestBooleanSelector.xml|gxml
        <Boolean Name="selector">
            <pValue>regSelector</pValue>
            <OnValue>0x1000</OnValue>
            <OffValue>0x2000</OffValue>
                <pSelected>UserSetVersion</pSelected>
        </Boolean>
        <IntReg Name="regSelector">
            <Address>0x0</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>myPort</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
        <Integer Name="UserSetVersion">
            <pValue>rVersion</pValue>
        </Integer>
        <IntReg Name="rVersion">
            <pAddress>regSelector</pAddress>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>myPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
        <Port Name="myPort"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestBooleanSelector")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x0, "uint32_t", 0x1000, RW, LittleEndian)
        Port.CreateEntry(0x1000, "int32_t", 42, RW, LittleEndian)
        Port.CreateEntry(0x2000, "int32_t", 24, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Selector = Camera.GetNode("selector")

        self.assertTrue(Selector.Node.IsSelector())
        selected = Selector.Node.GetSelectedFeatures()
        self.assertEqual(1, len(selected))
        Node01 = selected[0].GetNode()

        name01 = "UserSetVersion"
        self.assertEqual(name01, Node01.GetName())

    def test_Selecting(self):

        # create and initialize node map
        """[ GenApiTest@SelectorTestSuite_TestSelecting.xml|gxml
    
            <Category Name="Root">
                <pFeature>Feature</pFeature>
            </Category>
    
            <Integer Name="Feature">
                <Value>0</Value>
                <pSelected>Changer</pSelected>
            </Integer>
    
            <Integer Name="Changer">
                <Value>0</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef("TestCamera")
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelecting")

        print("Dumping PropertyNames:\n")
        Nodes = Camera._GetNodes()
        for Node in Nodes:
            print("Node '", Node.Node.GetName(), "'\n")

            PropertyNames = Node.Node.GetPropertyNames()

            for Property in PropertyNames:
                try:
                    ValueStr, AttributeStr = Node.Node.GetProperty(Property)
                except LogicalErrorException:
                    print("\t  Property '", Property, "' is not available\n")
                if AttributeStr == "":
                    print("\t  Property '", Property, "' = '", ValueStr, "'\n")
                else:
                    print("\t  Property '", Property, "' = '", ValueStr, "' [", AttributeStr, "]\n")

    # see #555
    def test_SelectorPropagation(self):

        # create and initialize node map
        """[ GenApiTest@SelectorTestSuite_TestSelectorPropagation.xml|gxml
    
            <Integer Name="NodeA">
                <Value>0</Value>
            </Integer>
    
            <Integer Name="NodeB">
                <pValue>NodeA</pValue>
            </Integer>
    
            <!--  note that schema v1.0 does allow pInvalidator nodes only on registers -->
            <IntReg Name="NodeC">
                <Address>0x0000</Address>
                <Length>8</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <pInvalidator>NodeA</pInvalidator>
                <Sign>Signed</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <Port Name="Port" >
            </Port>
    
            <Integer Name="NodeS">
                <Value>0</Value>
                <pSelected>NodeA</pSelected>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SelectorTestSuite_TestSelectorPropagation")

        Nodes = Camera._GetNodes()
        for Node in Nodes:
            print("-------------------------------")
            print("Node = '%s'", Node.Node.GetName())
            Selector = Node

            SelectedFeatures = Selector.Node.GetSelectedFeatures()
            for Feature in SelectedFeatures:
                print("pSelected = '", Feature.GetNode().GetName(), "'")
                pass

            SelectingFeatures = Selector.Node.GetSelectingFeatures()
            for Feature in SelectingFeatures:
                print("pSelecting = '", Feature.GetNode().GetName(), "'")
                pass

            if Node.Node.GetName() == "NodeA":
                self.assertTrue(len(SelectedFeatures) == 0 and len(SelectingFeatures) == 1 and SelectingFeatures[
                    0].GetNode().GetName() == "NodeS")

            if Node.Node.GetName() == "NodeB":
                self.assertTrue(len(SelectedFeatures) == 0 and len(SelectingFeatures) == 1 and SelectingFeatures[
                    0].GetNode().GetName() == "NodeS")

            if Node.Node.GetName() == "NodeC":
                self.assertTrue(len(SelectedFeatures) == 0 and len(SelectingFeatures) == 0)

            if Node.Node.GetName() == "NodeS":
                self.assertTrue(len(SelectedFeatures) == 2 and SelectedFeatures[0].GetNode().GetName() == "NodeA"
                                and SelectedFeatures[1].GetNode().GetName() == "NodeB"
                                and len(SelectingFeatures) == 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
