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
from testport import CTestPort, cast_data, cast_buffer, CStructTestPort
from callbackhelper import CallbackTestTarget


class EnumerationTestSuite(GenicamTestCase):
    FLOAT32_EPSILON = 1.19209e-07  # np.finfo(np.float32).eps
    FLOAT64_EPSILON = 2.22044604925e-16  # np.finfo(float).eps

    def test_ValueAccess(self):
        """[ GenApiTest@EnumerationTestSuite_TestValueAccess.xml|gxml
    
            <Enumeration Name="Enum">
                <EnumEntry Name="EnumValue1">
                    <Value>10</Value>
               </EnumEntry>
                <EnumEntry Name="EnumValue2">
                    <Value>20</Value>
               </EnumEntry>
                <pValue>Value</pValue>
            </Enumeration>
    
            <Integer Name="Value">
                <Value>10</Value>
            </Integer>
    
            <Enumeration Name="Enum2">
                <pIsLocked>Lock</pIsLocked>
                <EnumEntry Name="EnumValue1">
                    <Value>10</Value>
               </EnumEntry>
                <EnumEntry Name="EnumValue2">
                    <Value>20</Value>
               </EnumEntry>
                <EnumEntry Name="EnumValue3">
                    <pIsAvailable>False</pIsAvailable>
                    <Value>30</Value>
               </EnumEntry>
                <pValue>Value2</pValue>
            </Enumeration>
    
            <IntReg Name="Value2">
                <Address>0</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <Sign>Signed</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <Integer Name="False">
                <Value>0</Value>
            </Integer>
    
           <Integer Name="Lock">
               <Value>0</Value>
           </Integer>
    
            <Port Name="Port"/>
        """

        # LOG4CPP_NS::Category *pLogger = &CLog::GetLogger( "CppUnit.Performance" )

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestValueAccess")

        Enum = Camera.GetNode("Enum")
        self.assertEqual(intfIEnumeration, Enum.GetNode().GetPrincipalInterfaceType())

        Value = Camera.GetNode("Value")

        # happy path
        Enum.FromString("EnumValue1")
        self.assertEqual("EnumValue1", Enum.ToString())
        self.assertEqual(10, Value.GetValue())

        Enum.FromString("EnumValue2")
        self.assertEqual("EnumValue2", Enum.ToString())
        self.assertEqual(20, Value.GetValue())

        EnumEntry = Enum.GetCurrentEntry()
        print(EnumEntry)
        self.assertEqual("EnumValue2", EnumEntry.GetSymbolic())

        # Ahaem - this should not change over time :-)
        EnumEntry.GetNode().InvalidateNode()
        self.assertEqual(RO, EnumEntry.GetAccessMode())
        self.assertEqual(RO, EnumEntry.GetAccessMode())

        # value too small
        with self.assertRaises(InvalidArgumentException):   Enum.FromString("BlaBla")

        # GCLOGINFO( pLogger, "-------------------------------------------------")
        # GCLOGINFO( pLogger, "Setup : Enumeration <=> Integer")

        Value.GetNode().InvalidateNode()
        # TEST_BEGIN(1000)
        Enum.FromString("EnumValue1")
        # StopWatch.PauseBegin()
        Value.GetNode().InvalidateNode()
        # StopWatch.PauseEnd()
        # TEST_END( Enumeration::FromString )

        # now some tests with the other enum, connected to a real port
        Port = CTestPort()
        Port.CreateEntry(0x000, "int32_t", 10, RW, LittleEndian)
        Camera._Connect(Port, "Port")
        Enum2 = Camera.GetNode("Enum2")
        self.assertEqual(10, Enum2.GetIntValue())
        # modify the underlying value, not visible through the cache
        Value = 20
        Port.Write(0x00, cast_data("uint32_t", LittleEndian, Value))
        self.assertEqual(10, Enum2.GetIntValue())
        self.assertEqual("EnumValue1", Enum2.ToString())
        # but visible when bypassing the cache
        self.assertEqual(20, Enum2.GetIntValue(False, True))
        self.assertEqual("EnumValue2", Enum2.ToString(False, True))
        # now change it to point to the NA entry
        Value = 30
        Port.Write(0x00, cast_data("uint32_t", LittleEndian, Value))
        # and test without/with verification
        self.assertEqual(30, Enum2.GetIntValue(False, True))
        with self.assertRaises(AccessException):   Enum2.SetIntValue(30)
        self.assertEqual("EnumValue3", Enum2.ToString(False, True))
        with self.assertRaises(GenericException):
            Enum2.GetIntValue(True, True)
        with self.assertRaises(GenericException):
            Enum2.ToString(True, True)

    def test_EnumEntry(self):
        # (one of the Enumerations is a terminal node, the other not)
        """[ GenApiTest@EnumerationTestSuite_TestEnumEntry.xml|gxml
    
            <Enumeration Name="Value">
                <EnumEntry Name="MyEnumEntry0">
                    <Value>0</Value>
                </EnumEntry>
                <EnumEntry Name="MyEnumEntry1">
                    <Value>1</Value>
                </EnumEntry>
                <EnumEntry Name="MyEnumEntry2">
                    <Value>2</Value>
                </EnumEntry>
                <EnumEntry Name="MyEnumEntry3">
                    <pIsAvailable>EntryAvailable</pIsAvailable>
                    <Value>3</Value>
                </EnumEntry>
                <EnumEntry Name="MyEnumEntry4">
                    <pIsImplemented>EntryImplemented</pIsImplemented>
                    <Value>4</Value>
                </EnumEntry>
                <pValue>Value2</pValue>
            </Enumeration>
    
            <Integer Name="EntryAvailable">
                <Value>0</Value>
            </Integer>
    
            <Integer Name="EntryImplemented">
                <Value>0</Value>
            </Integer>
    
            <Integer Name="Value2">
                <Value>10</Value>
            </Integer>
    
            <Enumeration Name="OtherValue">
                <EnumEntry Name="MyOtherEnumEntry0">
                    <Value>0</Value>
                </EnumEntry>
                <EnumEntry Name="MyOtherEnumEntry1">
                    <Value>1</Value>
                </EnumEntry>
                <Value>0</Value>
            </Enumeration>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestEnumEntry")

        featureNode = Camera.GetNode("Value")
        Feature = featureNode
        if (Feature):
            # IEnumeration* pEnumeration =  dynamic_cast<IEnumeration*>(featureNode)
            # if (pEnumeration  not = NULL)
            # {
            #    gcstring_vector symbolics
            #    pEnumeration.GetSymbolics(symbolics)
            #    int i=0
            #    self.assertEqual( (int)symbolics.size(), 3 )
            #    self.assertEqual( gcstring("MyEnumEntry0"), symbolics[i++] )
            #    self.assertEqual( gcstring("MyEnumEntry1"), symbolics[i++] )
            #    self.assertEqual( gcstring("MyEnumEntry2"), symbolics[i++] )
            # }
            pass

        Value = Camera.GetNode("Value")

        Value.FromString("MyEnumEntry1")
        gstr = "MyEnumEntry1"
        self.assertEqual(gstr, Value.ToString())

        Value.FromString("MyEnumEntry2")
        gstr = "MyEnumEntry2"
        self.assertEqual(gstr, Value.ToString())

        Value.FromString("MyEnumEntry0")
        gstr = "MyEnumEntry0"
        self.assertEqual(gstr, Value.ToString())

        MyEntry = Value.GetEntryByName("MyEnumEntry1")
        #    self.assertEqual( (gcstring)"1", MyEntry.ToString(MyEntry.GetValue()) ) # *JS* removed warning
        self.assertEqual("1", MyEntry.ToString(MyEntry.GetValue() != 0))
        #    gcstring str = MyEntry.ToString( MyEntry.GetValue() ) # *JS* removed warning
        Str = MyEntry.ToString(MyEntry.GetValue() != 0)
        print(Str, type(Str))
        # entries are not writeable
        with self.assertRaises(GenericException):
            MyEntry.FromString(Str)

        gstr = MyEntry.GetSymbolic()
        self.assertEqual("MyEnumEntry1", gstr)

        # CEnumEntryRef refEnumEntry
        # self.assertTrue_NO_THROW(refEnumEntry.SetReference( Value ) )
        # with self.assertRaises( refEnumEntry.GetSymbolic()):  AccessException
        # with self.assertRaises( refEnumEntry.GetValue()):  AccessException
        # self.assertTrue_NO_THROW( refEnumEntry.SetReference( MyEntry ) )
        # self.assertEqual( (gcstring)"MyEnumEntry1", refEnumEntry.GetSymbolic())
        # self.assertEqual( 1,refEnumEntry.GetValue())
        # self.assertEqual (RO, refEnumEntry.GetAccessMode())

        # now do some additional tests with the terminal node
        Enum = Camera.GetNode("OtherValue")
        Enum.SetIntValue(1)
        self.assertEqual(1, Enum.GetIntValue())
        Enum.GetIntValue(True)

        with self.assertRaises(InvalidArgumentException):
            Enum.SetIntValue(100)
        # note that the Verify=False does not disable the checking against valid enum values...
        with self.assertRaises(InvalidArgumentException):
            Enum.SetIntValue(100, False)

        # what if value points to a NI entry?
        IntVal = Camera.GetNode("Value2")
        IntVal.SetValue(3)  # this entry is NA
        with self.assertRaises(AccessException):
            Value.ToString(True)
        with self.assertRaises(AccessException):
            Value.FromString("MyEnumEntry4")

    def test_EnumFalseEntry(self):
        """[ GenApiTest@EnumerationTestSuite_TestEnumFalseEntry.xml|gxml
            <Enumeration Name="NoValue">
                <EnumEntry Name="MyEnumEntry1">
                <Value>3</Value>
                </EnumEntry>
                <pValue>Value2</pValue>
            </Enumeration>
    
            <Integer Name="Value2">
                <Value>10</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestEnumFalseEntry")

        # gcstring_vector symbolics
        FalsePtr = Camera.GetNode("NoValue")
        self.assertEqual(RW, FalsePtr.GetAccessMode())
        symbolics = FalsePtr.GetSymbolics()
        with self.assertRaises(InvalidArgumentException):   FalsePtr.ToString()
        FalsePtr.SetIntValue(3)
        self.assertEqual("MyEnumEntry1", FalsePtr.ToString())

    def test_EnumRef(self):
        """[ GenApiTest@EnumerationTestSuite_TestEnumRef.xml|gxml
            <Enumeration Name="PixelFormat">
              <EnumEntry Name="Mono8">
                 <Value>0</Value>
              </EnumEntry>
              <EnumEntry Name="Mono16">
                 <Value>1</Value>
              </EnumEntry>
              <EnumEntry Name="RGB24">
                 <Value>2</Value>
              </EnumEntry>
              <pValue>Value</pValue>
            </Enumeration>
    
            <Integer Name="Value">
                <Value>10</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestEnumRef")

        Port = CTestPort()
        Port.CreateEntry(0x0104, "uint32_t", 1024, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Value = Camera.GetNode("PixelFormat")

        # not valid pointer for testing False cases
        # CEnumerationTRef<int> refFalse

        # CEnumerationTRef<int> refEnumT
        # self.assertTrue_NO_THROW( refEnumT.SetReference( Value ) )
        # self.assertTrue_NO_THROW( refEnumT.SetEnumReference(0, "PixelFormat" ) )

        # with self.assertRaises( refFalse.IsValueCacheValid()):  AccessException
        # self.assertTrue(  not refEnumT.IsValueCacheValid() )

        # Value = refEnumT.GetNode()
        # with self.assertRaises( refFalse.GetNode()):  AccessException

        # CEnumerationTRef<EAccessMode> refEnumAcc
        # EAccessMode AMode = RW
        # self.assertTrue_NO_THROW( refEnumAcc.GetAccessMode())
        # self.assertTrue_NO_THROW( refEnumAcc.SetReference( Value ) )
        # self.assertEqual( AMode, refEnumAcc.GetAccessMode())

        # gcstring_vector symbolics
        # with self.assertRaises( refFalse.GetSymbolics(symbolics)):  AccessException
        # refEnumT.GetSymbolics(symbolics)
        # int i(0)
        # self.assertEqual( gcstring("Mono8"), symbolics[i++] )
        # self.assertEqual( gcstring("Mono16"), symbolics[i++] )
        # self.assertEqual( gcstring("RGB24"), symbolics[i++] )
        # self.assertEqual( size_t(i), symbolics.size() )

        # NodeList_t entries
        # i=0
        # gcstring str1 = "EnumEntry_PixelFormat_Mono8",
        #    str2 = "EnumEntry_PixelFormat_Mono16",
        #    str3 = "EnumEntry_PixelFormat_RGB24"
        # with self.assertRaises( refFalse.GetEntries(entries)):  AccessException
        # refEnumT.GetEntries(entries)
        # self.assertEqual( str1, entries[i++].GetName() )
        # self.assertEqual( str2, entries[i++].GetName() )
        # self.assertEqual( str3, entries[i++].GetName() )
        # self.assertEqual( size_t(i), entries.size() )

        """* AH: no longer allowed since Mantis #9 is fixed.
        Value.SetIntValue(1234)  # AH: now checked in test EnumerationTestSuite::TestInvalidValues()
        self.assertEqual(  1234LL,refEnumT.GetIntValue() )
        """

        # with self.assertRaises( refFalse.SetIntValue(5432)):  AccessException

        """* AH: no longer allowed since Mantis #9 is fixed
        refEnumT.SetIntValue(5432) # AH: now checked in test EnumerationTestSuite::TestInvalidValues()
        self.assertEqual(  5432LL,refEnumT.GetIntValue() )
        """

        # with self.assertRaises( refFalse.GetEntry(0)):   GenericException
        # with self.assertRaises( refFalse.GetCurrentEntry()):   GenericException
        # with self.assertRaises( refFalse.GetEntry((int)0), GenericException ) # falls into the EnumT version of GetEntry (EnumT=int):   above

        # IEnumEntry *MyEntry
        # with self.assertRaises( refFalse.GetEntryByName("RGB24")):  AccessException
        # MyEntry = refEnumT.GetEntryByName("RGB24")
        # self.assertTrue(MyEntry)
        # self.assertEqual((gcstring)"2", MyEntry.ToString())

        #    self.assertEqual(  10LL, refEnumT.GetIntValue(MyEntry.GetValue())) # *JS* removed warning
        # with self.assertRaises( refEnumT.GetIntValue(MyEntry.GetValue()  not = 0)):   OutOfRangeException
        #    with self.assertRaises( refFalse.GetIntValue(MyEntry.GetValue())):  AccessException  # *JS* removed warning
        # with self.assertRaises( refFalse.GetIntValue(MyEntry.GetValue()  not = 0)):  AccessException

        # with self.assertRaises( refEnumT.ToString(0)):   InvalidArgumentException
        # refEnumT.SetIntValue(1)
        # self.assertEqual((gcstring)"Mono16",refEnumT.ToString(0) )
        # self.assertEqual ((gcstring)"Mono16",refEnumT.GetCurrentEntry().GetSymbolic())
        # self.assertEqual ((gcstring)"Mono8",refEnumT.GetEntry(0).GetSymbolic())
        # self.assertEqual ((IEnumEntry*)NULL,refEnumT.GetEntry(234))
        # with self.assertRaises( refFalse.ToString(0)):  AccessException

        # refEnumT.FromString("Mono8") # ???
        # with self.assertRaises( refFalse.FromString("Mono8")):  AccessException

        # with self.assertRaises( refEnumT.GetValue()):  AccessException

        # refEnumT.SetNumEnums(3)
        #   undef max
        # with self.assertRaises( refEnumT.SetValue(int(MyEntry.GetValue() & numeric_limits<unsigned>::max() ))):  AccessException
        # with self.assertRaises( refFalse.SetValue(int(MyEntry.GetValue() & numeric_limits<unsigned>::max() ))):  AccessException


        # With the fix of Mantis 376, the following assertion would fail.
        #    self.assertEqual( 0, refEnumT.GetValue() )

        # Since no enum references are set, GetValue() must throw an exception
        # with self.assertRaises( refEnumT.GetValue()):   AccessException  # checks if Mantis 376 works

        # with self.assertRaises( refFalse.GetValue()):  AccessException

        # refEnumT.SetEnumReference(0, "Mono8")
        # refEnumT.SetEnumReference(1, "Mono16")
        # refEnumT.SetEnumReference(2, "RGB24")

        # this one does nothing (the call is ignored), it is here just to complete the coverage
        # self.assertTrue_NO_THROW( refFalse.SetEnumReference(0, "FooBar") )

        # refEnumT.SetValue(1)
        # self.assertEqual( 1, refEnumT.GetValue() )
        # self.assertEqual (True, refEnumT.IsValueCacheValid())

        # refEnumT = "Mono16"
        # self.assertEqual( 1, refEnumT.GetIntValue() )
        # with self.assertRaises( refFalse = "Mono16"):   AccessException

        # refEnumT = gcstring("RGB24")
        # self.assertEqual( 2, refEnumT.GetIntValue() )
        # with self.assertRaises( refFalse = gcstring("Mono16")):   AccessException

        # self.assertEqual( gcstring("RGB24"), *refEnumT )
        # with self.assertRaises( *refFalse):   AccessException

        # self.assertEqual( 2, refEnumT() )
        # with self.assertRaises( refFalse()):  AccessException

        Camera.GetNode("PixelFormat")

    def test_DisplayName(self):
        """[ GenApiTest@EnumerationTestSuite_TestDisplayName.xml|gxml
            <Enumeration Name="Enumeration">
                <EnumEntry Name="EnumEntry0">
                    <Value>0</Value>
                </EnumEntry>
                <EnumEntry Name="EnumEntry1">
                    <Value>1</Value>
                    <Symbolic>Symbolic1</Symbolic>
                </EnumEntry>
                <EnumEntry Name="EnumEntry2">
                    <DisplayName>DisplayName2</DisplayName>
                    <Value>2</Value>
                </EnumEntry>
                <EnumEntry Name="EnumEntry3">
                    <DisplayName>DisplayName3</DisplayName>
                    <Value>3</Value>
                    <Symbolic>Symbolic3</Symbolic>
                </EnumEntry>
                <Value>0</Value>
            </Enumeration>
    
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestDisplayName")

        Enumeration = Camera.GetNode("Enumeration")
        # IEnumeration* pEnumeration =  dynamic_cast<IEnumeration*>(ValueNode)

        # self.assertTrue(dynamic_cast<INode*>(Enumeration.GetEntryByName("EnumEntry0")))
        # self.assertEqual (gcstring("EnumEntry0"), (dynamic_cast<INode*>(Enumeration.GetEntryByName("EnumEntry0"))).GetDisplayName() )
        # self.assertEqual ((IEnumEntry*)NULL, Enumeration.GetEntryByName("EnumEntry1") )
        # self.assertEqual (gcstring("Symbolic1"), (dynamic_cast<INode*>(Enumeration.GetEntryByName("Symbolic1"))).GetDisplayName() )
        # self.assertEqual (gcstring("DisplayName2"), (dynamic_cast<INode*>(Enumeration.GetEntryByName("EnumEntry2"))).GetDisplayName() )
        # self.assertEqual ((IEnumEntry*)NULL, Enumeration.GetEntryByName("EnumEntry3") )
        # self.assertEqual (gcstring("DisplayName3"), (dynamic_cast<INode*>(Enumeration.GetEntryByName("Symbolic3"))).GetDisplayName() )

    def test_NumericValue(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        # create and initialize node map
        """[ GenApiTest@EnumerationTestSuite_TestNumericValue.xml|gxml
    
            <Integer Name="IntFromEnum">
                <pValue>Enum</pValue>
            </Integer>
    
            <Enumeration Name="Enum">
                <EnumEntry Name="EnumValue1">
                    <Value>10</Value>
                    <NumericValue>1.5</NumericValue>
               </EnumEntry>
                <EnumEntry Name="EnumValue2">
                    <Value>20</Value>
               </EnumEntry>
                <EnumEntry Name="EnumValue3">
                    <Value>30</Value>
                    <NumericValue>1.7</NumericValue>
               </EnumEntry>
                <Value>10</Value>
            </Enumeration>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestNumericValue")

        Enum = Camera.GetNode("Enum")
        EnumEntry1 = Enum.GetEntryByName("EnumValue1")
        EnumEntry2 = Enum.GetEntryByName("EnumValue2")
        IntFromEnum = Camera.GetNode("IntFromEnum")

        self.assertAlmostEqual(1.5, EnumEntry1.GetNumericValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(20.0, EnumEntry2.GetNumericValue(), delta=self.FLOAT64_EPSILON)

        # the same through reference
        # CEnumEntryRef refEnumEntry1, refEnumEntry2
        # self.assertRaises (refEnumEntry1.GetNumericValue(), GenICam::AccessException)
        # self.assertTrue_NO_THROW(refEnumEntry1.SetReference( EnumEntry1 ) )
        # self.assertTrue_NO_THROW(refEnumEntry2.SetReference( EnumEntry2 ) )
        # self.assertAlmostEqual( 1.5, refEnumEntry1.GetNumericValue(), delta=self.FLOAT64_EPSILON )
        # self.assertAlmostEqual( 20.0, refEnumEntry2.GetNumericValue(), delta=self.FLOAT64_EPSILON )

        # try setting an enum through an integer
        IntFromEnum.SetValue(1)
        self.assertEqual("EnumValue1", Enum.ToString())
        IntFromEnum.SetValue(2)
        self.assertEqual("EnumValue3", Enum.ToString())
        IntFromEnum.SetValue(20)
        self.assertEqual("EnumValue2", Enum.ToString())

    # def TestAutoGain_Callback(INode *pNode)
    # {
    #    CValuePtr Value(pNode)
    #    Value.ToString()
    # }





    def test_AutoGain(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return
        """============ type definitions for the register space defined below ========== """

        class EGainAuto:
            Off = 1
            Once = 2
            Continuous = 3

        """============ Setup the register space ========== """
        regs = [("Gain", "uint32_t", 0, RW, LittleEndian),
                ("GainAutoReg", "uint8_t", 0, RW, LittleEndian),
                ]

        GainAutoFeaturePort = CStructTestPort(regs)
        GainAutoFeaturePort.Gain = 42
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        """============ Setup the corresponding XML file ========== """

        # create and initialize node map
        """[ GenApiTest@EnumerationTestSuite_TestAutoGain.xml|gxml
    
            <IntReg Name="Gain">
                <pBlockPolling>GainPollingBlock</pBlockPolling>
                <Address>0</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <PollingTime>1000</PollingTime>
                <Sign>Unsigned</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <IntReg Name="GainAutoReg">
                <Address>4</Address>
                <Length>1</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <Sign>Unsigned</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <Enumeration Name="GainAuto">
               <EnumEntry Name="Off">
                    <Value>1</Value>
               </EnumEntry>
               <EnumEntry Name="Once">
                    <Value>2</Value>
                    <IsSelfClearing>Yes</IsSelfClearing>
               </EnumEntry>
               <EnumEntry Name="Continuous">
                    <Value>3</Value>
               </EnumEntry>
               <pValue>GainAutoReg</pValue>
               <PollingTime>50</PollingTime>
            </Enumeration>
    
            <IntSwissKnife Name="GainPollingBlock">
                <pVariable Name="GainAuto">GainAuto</pVariable>
                <Formula> GainAuto=1 ? 1 : 0 </Formula>
            </IntSwissKnife>
    
            <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestAutoGain")
        Camera._Connect(GainAutoFeaturePort, "Port")

        """============ Get pointers and do basic checks ========== """

        Gain = Camera.GetNode("Gain")
        GainAuto = Camera.GetNode("GainAuto")

        self.assertEqual(42, Gain.GetValue(IgnoreCache=True))
        Gain.SetValue(4711)
        self.assertEqual(4711, Gain.GetValue())
        self.assertEqual(4711, GainAutoFeaturePort.Gain)

        self.assertEqual("Off", GainAuto.ToString())
        GainAuto.SetValue("Continuous")
        self.assertEqual("Continuous", GainAuto.ToString())
        self.assertEqual(EGainAuto.Continuous, (GainAutoFeaturePort.GainAutoReg))

        GainAutoOff = GainAuto.GetEntryByName("Off")
        GainAutoOnce = GainAuto.GetEntryByName("Once")

        self.assertEqual(False, GainAutoOff.IsSelfClearing())
        self.assertEqual(True, GainAutoOnce.IsSelfClearing())

        """============ Test basic auto-reset ========== """

        GainAutoCallback = CallbackTestTarget(GainAuto)

        # this callback will read the value
        # Register( GainAuto.GetNode(), TestAutoGain_Callback )

        # start one cycle of auto-gain
        GainAuto.SetValue("Once")
        self.assertEqual(EGainAuto.Once, (GainAutoFeaturePort.GainAutoReg))
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        # poll while waiting for the auto-gain cycle to complete
        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        Camera._Poll(25)
        self.assertTrue(not GainAutoCallback.HasFiredOnce())
        Camera._Poll(25)
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        # the camera signals we're ready
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasFiredOnce())
        self.assertEqual("Off", GainAuto.ToString())

        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasNotFired())

        """============ Test different use cases of auto-reset ========== """

        GainAuto.SetValue("Once")
        GainAutoCallback.Reset()
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        # "cleared" by setting another value
        GainAuto.SetValue("Continuous")
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        #######

        GainAuto.SetValue("Once")
        GainAutoCallback.Reset()
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        # "cleared" by setting another value
        GainAuto.SetIntValue(EGainAuto.Continuous)
        self.assertTrue(GainAutoCallback.HasFiredOnce())

        #######

        GainAuto.SetValue("Once")
        GainAuto.GetIntValue()
        GainAutoCallback.Reset()
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        # "cleared" by getting the value
        GainAuto.GetIntValue()
        # but no callback, since it is a read
        self.assertTrue(GainAutoCallback.HasNotFired())
        # no callback since it is cleared already
        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasNotFired())

        #######

        GainAuto.SetValue("Once")
        GainAutoCallback.Reset()
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off

        # "cleared" by getting the value
        GainAuto.ToString()
        # but no callback, since it is a read
        self.assertTrue(GainAutoCallback.HasNotFired())
        # no callback since it is cleared already
        Camera._Poll(100)
        self.assertTrue(GainAutoCallback.HasNotFired())

        """============ Test continuous ========== """
        GainAuto.SetValue("Continuous")

        GainAutoFeaturePort.Gain = 48
        GainCallback = CallbackTestTarget(Gain)
        Camera._Poll(100)
        self.assertTrue(GainCallback.HasNotFired())
        Camera._Poll(1000)
        self.assertTrue(GainCallback.HasFiredOnce())
        self.assertEqual(48, Gain.GetValue())

        """============ Test off ========== """

        GainAuto.SetValue("Off")
        GainCallback.Reset()

        # fill the cache and then change the register value
        self.assertEqual(48, Gain.GetValue())
        GainAutoFeaturePort.Gain = 49

        # now polling does not happen and the cache is not cleared
        Camera._Poll(2000)
        self.assertTrue(GainCallback.HasNotFired())
        # because the cache is enabled the old value is given
        self.assertEqual(48, Gain.GetValue())

        """============ Test caching, Continuous ========== """

        GainAuto.SetValue("Continuous")  # this clears the Gain cache
        GainAutoFeaturePort.Gain = 111
        self.assertEqual(111, Gain.GetValue())
        GainAutoFeaturePort.Gain = 222
        # Since there is no polling and Continuous is not self clearing anyway the cached value is
        # returned
        self.assertEqual(111, Gain.GetValue())

        """============ Test caching, Off ========== """
        GainAuto.SetValue("Off")  # this clears the Gain cache
        # this fills the cache
        self.assertEqual(222, Gain.GetValue())
        GainAutoFeaturePort.Gain = 333
        # value comes from cache
        self.assertEqual(222, Gain.GetValue())

        """============ Test caching, Once ========== """
        GainAuto.SetValue("Once")  # this clears the cache
        GainAutoFeaturePort.Gain = 444
        # this fills the cache
        self.assertEqual(444, Gain.GetValue())
        GainAutoFeaturePort.Gain = 555
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off
        # since Once is self clearing the value is read and Gain's cache is cleard
        self.assertEqual("Off", GainAuto.ToString())
        # this fills the cache
        self.assertEqual(555, Gain.GetValue())

        # once again without direct read of GainAuto
        GainAuto.SetValue("Once")  # this clears the Gain cache
        GainAutoFeaturePort.Gain = 666
        # this fills the cache
        self.assertEqual(666, Gain.GetValue())
        GainAutoFeaturePort.Gain = 777
        # since GainAuto is not read this goes unnotices
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off
        # value comes form cache
        self.assertEqual(666, Gain.GetValue())
        GainAutoFeaturePort.Gain = 888
        # value comes form cache
        self.assertEqual(666, Gain.GetValue())  # from cache

        """============ Test auto-reset, read before poll ========== """

        # start one cycle of auto-gain
        Gain.SetValue(123)
        self.assertEqual(123, Gain.GetValue())
        GainAutoCallback.Reset()
        GainCallback.Reset()
        GainAuto.SetValue("Once")
        self.assertEqual(EGainAuto.Once, (GainAutoFeaturePort.GainAutoReg))
        self.assertTrue(GainAutoCallback.HasFiredOnce())
        self.assertTrue(GainCallback.HasFiredOnce())
        self.assertEqual(123, Gain.GetValue())

        # the camera signals we're ready, get to know that through reading (before any poll)
        GainAutoFeaturePort.Gain = 234
        GainAutoFeaturePort.GainAutoReg = EGainAuto.Off
        self.assertEqual("Off", GainAuto.ToString())

        # polling does not fire any more
        Camera._Poll(1000)
        self.assertTrue(GainAutoCallback.HasNotFired())
        self.assertTrue(GainCallback.HasNotFired())

        # the callbacks do not come, but Gain value is still invalidated
        self.assertEqual(234, Gain.GetValue())

    def test_GetEntry(self):
        """[ GenApiTest@EnumerationTestSuite_TestGetEntry.xml|gxml
    
                <Enumeration Name="Enum">
                    <EnumEntry Name="EnumValue1">
                        <Value>10</Value>
                   </EnumEntry>
                    <EnumEntry Name="EnumValue2">
                        <Value>20</Value>
                   </EnumEntry>
                    <pValue>Value</pValue>
                </Enumeration>
    
                <Integer Name="Value">
                    <Value>10</Value>
                </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestGetEntry")

        Enum = Camera.GetNode("Enum")

        EnumEntry = Enum.GetEntry(20)
        self.assertEqual(20, EnumEntry.GetValue())

    def test_AccessMode(self):
        # create and initialize node map
        """[ GenApiTest@EnumerationTestSuite_TestAccessMode.xml|gxml
    
            <Enumeration Name="Enum">
                <EnumEntry Name="EnumEntry1">
                    <pIsImplemented>Toggle_I</pIsImplemented>
                    <pIsAvailable>Toggle_A</pIsAvailable>
                    <Value>10</Value>
                </EnumEntry>
                <EnumEntry Name="EnumEntry2">
                    <pIsImplemented>Toggle_I</pIsImplemented>
                    <pIsAvailable>Toggle_A</pIsAvailable>
                    <Value>20</Value>
                </EnumEntry>
                <Value>10</Value>
            </Enumeration>
    
            <Integer Name="Toggle_A">
               <Value>1</Value>
            </Integer>
    
            <Integer Name="Toggle_I">
               <Value>1</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestAccessMode")

        # Fetch node pointers
        Enum = Camera.GetNode("Enum")
        EnumEntry1 = Camera.GetNode("EnumEntry_Enum_EnumEntry1")
        EnumEntry2 = Camera.GetNode("EnumEntry_Enum_EnumEntry2")
        ToggleAvailabilty = Camera.GetNode("Toggle_A")
        ToggleImplementationAvailabilty = Camera.GetNode("Toggle_I")

        # What happens if both EnumEntries become not available?
        self.assertEqual(RW, Enum.GetAccessMode())
        ToggleAvailabilty.SetValue(0)
        self.assertEqual(NA, Enum.GetAccessMode())
        # Repeat the same test to see if correct access mode was cached
        self.assertEqual(NA, Enum.GetAccessMode())
        with self.assertRaises(GenericException):   Enum.GetIntValue()
        ToggleAvailabilty.SetValue(1)
        self.assertEqual(RW, Enum.GetAccessMode())

        # What happens if both EnumEntries become not implemented?
        self.assertEqual(RW, Enum.GetAccessMode())
        ToggleImplementationAvailabilty.SetValue(0)
        self.assertEqual(NI, Enum.GetAccessMode())
        ToggleImplementationAvailabilty.SetValue(1)
        self.assertEqual(RW, Enum.GetAccessMode())

        # Same questions but triggered using ImposeAccessMode
        self.assertEqual(RW, Enum.GetAccessMode())
        Enum.GetNode().ImposeAccessMode(RO)
        self.assertEqual(RO, Enum.GetAccessMode())
        EnumEntry1.GetNode().ImposeAccessMode(NA)
        self.assertEqual(RO, Enum.GetAccessMode())
        EnumEntry2.GetNode().ImposeAccessMode(NA)
        self.assertEqual(NA, Enum.GetAccessMode())
        EnumEntry1.GetNode().ImposeAccessMode(NI)
        self.assertEqual(NA, Enum.GetAccessMode())
        EnumEntry2.GetNode().ImposeAccessMode(NI)
        self.assertEqual(NI, Enum.GetAccessMode())

    def test_Ticket778(self):
        # create and initialize node map
        """[ GenApiTest@EnumerationTestSuite_TestTicket778.xml|gxml
    
            <Enumeration Name="EnumA">
                <EnumEntry Name="EnumValue1">
                    <pIsAvailable>AvailableA</pIsAvailable>
                    <Value>10</Value>
                </EnumEntry>
                <EnumEntry Name="EnumValue2">
                    <Value>20</Value>
                </EnumEntry>
                <Value>10</Value>
            </Enumeration>
    
            <Enumeration Name="EnumB">
                <EnumEntry Name="EnumValue1">
                    <pIsAvailable>AvailableB</pIsAvailable>
                    <Value>10</Value>
                </EnumEntry>
                <EnumEntry Name="EnumValue2">
                    <Value>20</Value>
                </EnumEntry>
                <Value>10</Value>
            </Enumeration>
    
            <IntReg Name="AvailableA">
                <Address>0</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <Cachable>NoCache</Cachable>
                <Sign>Signed</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <IntReg Name="AvailableB">
                <Address>0</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <Cachable>WriteThrough</Cachable>
                <Sign>Signed</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "EnumerationTestSuite_TestTicket778")

        EnumA = Camera.GetNode("EnumA")
        EnumEntry_EnumA_EnumValue1 = Camera.GetNode("EnumEntry_EnumA_EnumValue1")
        EnumEntry_EnumA_EnumValue2 = Camera.GetNode("EnumEntry_EnumA_EnumValue2")
        AvailableA = Camera.GetNode("AvailableA")

        EnumB = Camera.GetNode("EnumB")
        EnumEntry_EnumB_EnumValue1 = Camera.GetNode("EnumEntry_EnumB_EnumValue1")
        EnumEntry_EnumB_EnumValue2 = Camera.GetNode("EnumEntry_EnumB_EnumValue2")
        AvailableB = Camera.GetNode("AvailableB")

        self.assertEqual(NoCache, AvailableA.GetNode().GetCachingMode())
        self.assertEqual(WriteThrough, AvailableB.GetNode().GetCachingMode())

        self.assertEqual(No, EnumEntry_EnumA_EnumValue1.GetNode().IsAccessModeCacheable())
        self.assertEqual(Yes, EnumEntry_EnumB_EnumValue1.GetNode().IsAccessModeCacheable())

        self.assertEqual(Yes, EnumEntry_EnumA_EnumValue2.GetNode().IsAccessModeCacheable())
        self.assertEqual(Yes, EnumEntry_EnumB_EnumValue2.GetNode().IsAccessModeCacheable())

        self.assertEqual(No, EnumA.GetNode().IsAccessModeCacheable())
        self.assertEqual(Yes, EnumB.GetNode().IsAccessModeCacheable())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'EnumerationTestSuite.test_AccessMode_issue_711']
    unittest.main()
