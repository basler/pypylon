import unittest
from pypylon import genicam

class PylonParameterTestCase(unittest.TestCase):
    nodemapref = None
    nodemap = None

    def _destroy_nodemapref_if_needed(self):
        nodemapref = getattr(self, "nodemapref", None)
        if nodemapref is not None:
            nodemapref._Destroy()
            self.nodemapref = None
        self.nodemap = None

    def setUp(self):
        self._destroy_nodemapref_if_needed()
        self.nodemapref = self.create_nodemapref()
        self.nodemap = self.nodemapref._Ptr
    def tearDown(self):
        self._destroy_nodemapref_if_needed()

    def getINode(self, name):
        # nodemap.GetNode(name) automatically downcasts to the specific node type.
        # That's why we need to call GetNode() again to get the base INode.
        node = self.nodemap.GetNode(name).GetNode()
        if node is None:
            raise Exception(f"Node {name} not found in nodemap")
        return node

    def create_nodemapref(self):
        testCameraDescriptionFile = """\
<?xml version="1.0" encoding="utf-8"?>
<RegisterDescription
      ModelName="GenApiTest"
      VendorName="Generic"
      ToolTip="nodes for testing"
      StandardNameSpace="GEV"
      SchemaMajorVersion="1"
      SchemaMinorVersion="1"
      SchemaSubMinorVersion="0"
      MajorVersion="2"
      MinorVersion="3"
      SubMinorVersion="4"
      ProductGuid="2D932CC6-EB68-40bd-B6CC-F03B55B7D653"
      VersionGuid="02A8C268-BEE8-463b-A6C0-53ED8256E3D8"
      xmlns="http://www.genicam.org/GenApi/Version_1_1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.genicam.org/GenApi/Version_1_1
            http://www.genicam.org/GenApi/GenApiSchema_Version_1_1.xsd">

  <Register Name="RegisterA">
    <Address>0x80</Address>
    <Length>4</Length>
    <AccessMode>RW</AccessMode>
    <pPort>Device</pPort>
  </Register>

  <Register Name="RegisterB">
    <Address>0x90</Address>
    <Length>2</Length>
    <AccessMode>RW</AccessMode>
    <pPort>Device</pPort>
  </Register>

  <Port Name="Device" NameSpace="Standard">
    <ToolTip> Port giving access to the camera. </ToolTip>
  </Port>


  <Boolean Name="TestpIsAvailable">
    <Value>1</Value>
  </Boolean>
  <Boolean Name="TestpIsNotAvailable">
    <Value>0</Value>
  </Boolean>

  <Boolean Name="TestpIsImplemented">
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestpIsNotImplemented">
    <Value>0</Value>
  </Boolean>

  <Boolean Name="TestpIsLocked">
    <Value>1</Value>
  </Boolean>
  <Boolean Name="TestpIsNotLocked">
    <Value>0</Value>
  </Boolean>

  <!--Initialize Int parameters-->

  <Integer Name="TestIntRO">
    <ImposedAccessMode>RO</ImposedAccessMode>
    <Value>1500</Value>
    <Min>1000</Min>
    <Max>2000</Max>
    <Inc>4</Inc>
  </Integer>

  <Integer Name="TestIntWO">
    <ImposedAccessMode>WO</ImposedAccessMode>
    <Value>1500</Value>
    <Min>1000</Min>
    <Max>2000</Max>
    <Inc>4</Inc>
  </Integer>

  <Integer Name="TestInt">
       <Value>1500</Value>
       <Min>1000</Min>
       <Max>2000</Max>
       <Inc>4</Inc>
       <Unit>eggs</Unit>
   </Integer>

   <Integer Name="TestIntCorrectionInc1">
     <Value>10</Value>
     <Min>10</Min>
     <Max>100</Max>
     <Inc>1</Inc>
   </Integer>

   <Integer Name="TestIntCorrectionInc3">
     <Value>10</Value>
     <Min>10</Min>
     <Max>100</Max>
     <Inc>3</Inc>
   </Integer>

   <Integer Name="TestIntCorrectionInc10">
     <Value>10</Value>
     <Min>10</Min>
     <Max>100</Max>
     <Inc>10</Inc>
   </Integer>

   <Integer Name="TestNegIntCorrectionInc10">
     <Value>10</Value>
     <Min>-100</Min>
     <Max>-10</Max>
     <Inc>10</Inc>
   </Integer>

   <Integer Name="TestArounZeroIntCorrectionInc10">
     <Value>10</Value>
     <Min>-95</Min>
     <Max>95</Max>
     <Inc>10</Inc>
   </Integer>

   <Integer Name="TestPercentOfRangeInt">
       <Value>100</Value>
       <Min>100</Min>
       <Max>100</Max>
       <Inc>1</Inc>
   </Integer>

   <Integer Name="TestIntInvalid">
       <Value>2004</Value>
       <Min>1000</Min>
       <Max>2000</Max>
       <Inc>4</Inc>
   </Integer>

   <Integer Name="TestInt2" NameSpace="Custom">
       <Value>1234</Value>
   </Integer>
  <!---->

  <!--Initialize Float parameters-->
  <Float Name="TestFloatRW">
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1250</Value>
    <Min>1000</Min>
    <Max>2000</Max>
    <Inc>2</Inc>
  </Float>

  <Float Name="TestFloatRO">
    <ImposedAccessMode>RO</ImposedAccessMode>
    <Value>1234.5</Value>
    <Min>1</Min>
    <Max>9999</Max>
  </Float>

   <Float Name="TestFloatWO">
     <ImposedAccessMode>WO</ImposedAccessMode>
     <Value>123.123</Value>
   </Float>

  <Float Name="TestFloat">
    <Value>3.0</Value>
    <Min>2.71828</Min>
    <Max>3.14159</Max>
    <Unit>eggs</Unit>
  </Float>

  <Converter Name="TestFloat2">
    <pAlias>TestInt2</pAlias>
    <FormulaTo>FROM*10</FormulaTo>
    <FormulaFrom>TO/10</FormulaFrom>
    <pValue>TestInt2</pValue>
    <Unit>dB</Unit>
    <Representation>Linear</Representation>
    <Slope>Increasing</Slope>
  </Converter>
  <!---->

<Boolean Name="TestBoolRO">
       <ImposedAccessMode>RO</ImposedAccessMode>
       <Value>1</Value>
       <OnValue>1</OnValue>
       <OffValue>0</OffValue>
</Boolean>
<Boolean Name="TestBoolRW">
  <ToolTip>TestBoolRW Tooltip</ToolTip>
  <Description>TestBoolRW Description</Description>
  <DisplayName>TestBooleanRW Display Name</DisplayName>
    <Visibility>Beginner</Visibility>
    <!--<DocuURL>TestBoolRW DocuURL</DocuURL>-->
    <IsDeprecated>No</IsDeprecated>
       <ImposedAccessMode>RW</ImposedAccessMode>
    <Streamable>No</Streamable>
       <Value>0</Value>
       <OnValue>1</OnValue>
       <OffValue>0</OffValue>
</Boolean>
<Boolean Name="TestBoolWO">
       <ImposedAccessMode>WO</ImposedAccessMode>
       <Value>0</Value>
       <OnValue>1</OnValue>
       <OffValue>0</OffValue>
</Boolean>

  <Boolean Name="TestBoolNA">
    <pIsAvailable>TestpIsNotAvailable</pIsAvailable>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestBoolNI">
    <pIsImplemented>TestpIsNotImplemented</pIsImplemented>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>


  <Boolean Name="TestBoolLocked">
    <pIsLocked>TestpIsLocked</pIsLocked>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestBoolBeginner">
    <Visibility>Beginner</Visibility>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestBoolExpert">
    <Visibility>Expert</Visibility>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestBoolGuru">
    <Visibility>Guru</Visibility>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

  <Boolean Name="TestBoolInvisible">
    <Visibility>Invisible</Visibility>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>


  <Boolean Name="TestAdvancedPropertiesParameter">
    <Description>TestAdvancedPropertiesParameter description</Description>
    <DisplayName>TestAdvancedPropertiesParameter name</DisplayName>
    <Visibility>Beginner</Visibility>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>1</Value>
  </Boolean>

   <Port Name="TestPort">
     <ToolTip>TestPort ToolTip</ToolTip>
     <Description>TestPort Description</Description>
     <DisplayName>TestPort Display Name</DisplayName>
   </Port>
   <Port Name="TestChunkPort">
     <ChunkID>42</ChunkID>
   </Port>
   <IntReg Name="IntChild" >
       <Address>0</Address>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>TestPort</pPort>
       <PollingTime>2147483648</PollingTime>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
   </IntReg>
   <IntReg Name="IntParent" >
       <pAlias>IntChild</pAlias>
       <pAddress>IntChild</pAddress>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>TestPort</pPort>
       <PollingTime>2147483647</PollingTime>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
   </IntReg>
   <Integer Name="CommandInt">
       <Value>0</Value>
   </Integer>

  <!--Initialize command parameters-->
   <Command Name="TestCommand">
       <pValue>CommandInt</pValue>
       <CommandValue>4711</CommandValue>
   </Command>
   <Command Name="DeviceReset">
       <pValue>CommandInt</pValue>
       <CommandValue>4711</CommandValue>
   </Command>
  <Command Name="TestCommandWO">
    <ImposedAccessMode>WO</ImposedAccessMode>
    <pValue>CommandInt</pValue>
    <CommandValue>4711</CommandValue>
  </Command>
  <Command Name="TestCommandRO">
    <ImposedAccessMode>RO</ImposedAccessMode>
    <pValue>CommandInt</pValue>
    <CommandValue>1234</CommandValue>
  </Command>
  <!---->

  <!--Initialize string parameters-->
  <String Name="TestStringRW">
    <ImposedAccessMode>RW</ImposedAccessMode>
    <Value>TestStringValueRW</Value>
  </String>
  <String Name="TestStringRO">
    <ImposedAccessMode>RO</ImposedAccessMode>
    <Value>TestStringValueRO</Value>
  </String>
  <String Name="TestStringWO">
    <ImposedAccessMode>WO</ImposedAccessMode>
    <Value>TestStringValueWO</Value>
  </String>
  <!---->

  <!--Initialize enumeration parameters-->
  <Enumeration Name="TestEnumerationNI">
    <pIsImplemented>TestpIsNotImplemented</pIsImplemented>
    <ImposedAccessMode>RW</ImposedAccessMode>
    <EnumEntry Name="EntryTic">
      <Value>0</Value>
      <Symbolic>tic</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryTac">
      <Value>1</Value>
      <Symbolic>tac</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryToe">
      <Value>2</Value>
      <Symbolic>toe</Symbolic>
    </EnumEntry>
    <Value>0</Value>
    <pSelected>TestEnumerationIntValue</pSelected>
  </Enumeration>
  <Enumeration Name="TestEnumerationRO">
    <ImposedAccessMode>RO</ImposedAccessMode>
    <EnumEntry Name="EntryTic">
      <Value>0</Value>
      <Symbolic>tic</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryTac">
      <Value>1</Value>
      <Symbolic>tac</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryToe">
      <Value>2</Value>
      <Symbolic>toe</Symbolic>
    </EnumEntry>
    <Value>0</Value>
    <pSelected>TestEnumerationIntValue</pSelected>
  </Enumeration>

  <Enumeration Name="TestEnumerationWO">
    <ImposedAccessMode>WO</ImposedAccessMode>
    <EnumEntry Name="EntryTic">
      <Value>0</Value>
      <Symbolic>tic</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryTac">
      <Value>1</Value>
      <Symbolic>tac</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryToe">
      <Value>2</Value>
      <Symbolic>toe</Symbolic>
    </EnumEntry>
    <Value>0</Value>
    <pSelected>TestEnumerationIntValue</pSelected>
  </Enumeration>

  <Enumeration Name="TestEnumerationRW">
    <EnumEntry Name="EntryTic">
        <Value>0</Value>
        <Symbolic>tic</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryTac">
        <Value>1</Value>
        <Symbolic>tac</Symbolic>
    </EnumEntry>
    <EnumEntry Name="EntryToe">
        <Value>2</Value>
        <Symbolic>toe</Symbolic>
    </EnumEntry>
    <Value>0</Value>
    <pSelected>TestEnumerationIntValue</pSelected>
  </Enumeration>

  <Integer Name="TestEnumerationIntValue">
       <Value>0</Value>
       <Min>0</Min>
       <Max>2</Max>
  </Integer>
<!---->


   <Category Name="NestedCategory" >
    <pFeature>TestEnumerationRW</pFeature>
   </Category>
   <Category Name="Root" >
       <pFeature>NestedCategory</pFeature>
       <pFeature>TestFloat</pFeature>
       <pFeature>TestInt</pFeature>
   </Category>

<Integer Name="ROAvailability">
    <Value>0</Value>
  </Integer>
<Integer Name="RWAvailability">
    <Value>1</Value>
  </Integer>

</RegisterDescription>
"""
        nodemapref = genicam.CNodeMapRef()
        nodemapref._LoadXMLFromString(testCameraDescriptionFile)
        return nodemapref

