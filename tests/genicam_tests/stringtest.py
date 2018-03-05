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


class StringTestSuite(GenicamTestCase):
    def test_ValueAccess(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@StringTestSuite_TestValueAccess.xml|gxml
    
        <String Name="A">
            <Value>Alle meine Entchen...</Value>
        </String>
    
        <String Name="RO">
            <ImposedAccessMode>RO</ImposedAccessMode>
            <Value>Alle meine Ganschen...</Value>
        </String>
    
        <String Name="WO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <Value>Alle meine Ganschen...</Value>
        </String>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StringTestSuite_TestValueAccess")

        A = Camera.GetNode("A")
        # CPPUNIT_ASSERT( (bool) A )
        self.assertEqual(intfIString, A.GetNode().GetPrincipalInterfaceType())
        self.assertEqual("Alle meine Entchen...", A.GetValue())

        A.SetValue("...schwimmen auf dem See!")
        self.assertEqual("...schwimmen auf dem See!", A.GetValue())

        A.FromString("Ehh? Don't understand Hungarian...")
        self.assertEqual("Ehh? Don't understand Hungarian...", A.ToString())

        # excercise also strings with non-RW access mode
        RO = Camera.GetNode("RO")
        # CPPUNIT_ASSERT( (bool) ptrRO )
        self.assertEqual("Alle meine Ganschen...", RO.GetValue())
        with self.assertRaises(AccessException):
            RO.FromString("Ehh? Don't understand Hungarian...")
        self.assertEqual("Alle meine Ganschen...", RO.ToString())
        RO.GetMaxLength()

        WO = Camera.GetNode("WO")
        # CPPUNIT_ASSERT( (bool) ptrWO )
        # note that the access mode is checked only because Verify==True
        with self.assertRaises(AccessException):
            WO.GetValue(True)
        WO.FromString("Hmmm, how will I verify this value?")
        # note that the access mode is checked only because Verify==True
        with self.assertRaises(AccessException):
            WO.ToString(True)

            # cout << "MaxLength = " << ptrA.GetMaxLength() << "\n"
            # gcstring Dummy
            # self.assertEqual( (int64_t)Dummy.max_size(), ptrA.GetMaxLength())

    def test_PValueAccess(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@StringTestSuite_TestPValueAccess.xml|gxml
    
        <String Name="A">
            <Value>Hopsa hejsa do Brandejsa...</Value>
        </String>
    
        <String Name="B">
            <pValue>A</pValue>
        </String>
    
        <String Name="C">
            <pValue>B</pValue>
        </String>
        <String Name="D">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <pValue>A</pValue>
        </String>
    
        <String Name="E">
            <pValue>D</pValue>
        </String>
    
        <String Name="F">
            <ImposedAccessMode>RO</ImposedAccessMode>
            <pValue>A</pValue>
        </String>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StringTestSuite_TestPValueAccess")

        A = Camera.GetNode("A")
        self.assertEqual("Hopsa hejsa do Brandejsa...", A.GetValue())

        C = Camera.GetNode("C")
        self.assertEqual("Hopsa hejsa do Brandejsa...", C.GetValue())

        C.SetValue("...Brandejs nad Labem, to se nadlabem!")
        # <String> nodes with <pValue> entry to not have a cache. So they return the cache state of the node referred to
        self.assertEqual(True, C.IsValueCacheValid())
        self.assertEqual("...Brandejs nad Labem, to se nadlabem!", C.GetValue())
        self.assertEqual(True, C.IsValueCacheValid())
        self.assertEqual("...Brandejs nad Labem, to se nadlabem!", A.GetValue())

        # and test also the properties
        PropertyNames = A.Node.GetPropertyNames()
        """
        Dumping PropertyNames:
        Property 'DeviceName' = 'Device'
        Property 'ExposeStatic' = 'Yes'
        Property 'ImposedAccessMode' = 'RW'
        Property 'IsDeprecated' = 'No'
        Property 'IsFeature' = 'No'
        Property 'Name' = 'A'
        Property 'NameSpace' = 'Custom'
        Property 'Streamable' = 'No'
        Property 'Value' = '...Brandejs nad Labem, to se nadlabem!'
        Property 'Visibility' = 'Beginner'
        Property 'pDependent' = 'F      E       D       C       B'
        Property 'pTerminal' = 'A'    
        """
        print("Dumping PropertyNames:\n")
        for p_name in PropertyNames:
            print("-->", p_name)
            try:
                ValueStr, AttributeStr = A.Node.GetProperty(p_name)
                if (AttributeStr == ""):
                    print("\tProperty %s = %s\n" % (p_name, ValueStr))
                else:
                    print("\tProperty %s = %s [%s]\n" % (p_name, ValueStr, AttributeStr))

            except LogicalErrorException:
                print("\tProperty %s is not available\n" % (p_name))

        ValueStr, AttributeStr = A.Node.GetProperty("DeviceName")
        self.assertEqual("Device", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("ExposeStatic")
        self.assertEqual("Yes", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("ImposedAccessMode")
        self.assertEqual("RW", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("IsDeprecated")
        self.assertEqual("No", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("IsFeature")
        self.assertEqual("No", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("Name")
        self.assertEqual("A", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("Streamable")
        self.assertEqual("No", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("NameSpace")
        self.assertEqual("Custom", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("Value")
        self.assertEqual("...Brandejs nad Labem, to se nadlabem!", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("Visibility")
        self.assertEqual("Beginner", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("pDependent")
        self.assertEqual("F\tE\tD\tC\tB", ValueStr)
        self.assertEqual("", AttributeStr)

        ValueStr, AttributeStr = A.Node.GetProperty("pTerminal")
        self.assertEqual("A", ValueStr)
        self.assertEqual("", AttributeStr)

        # self.assertEqual( 22, C.GetMaxLength())

        E = Camera.GetNode("E")
        self.assertEqual(WO, E.GetAccessMode())

        F = Camera.GetNode("F")
        self.assertEqual(RO, F.GetAccessMode())
        self.assertEqual(len("...Brandejs nad Labem, to se nadlabem!"), F.GetMaxLength())

    def test_PValueAccessModeInheritance(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@StringTestSuite_TestPValueAccessModeInheritance.xml|gxml
    
        <String Name="RO">
            <ImposedAccessMode>RO</ImposedAccessMode>
            <Value>test read only...</Value>
        </String>
    
        <String Name="PRO">
            <pValue>RO</pValue>
        </String>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StringTestSuite_TestPValueAccessModeInheritance")

        nodeRO = Camera.GetNode("RO")
        # CPPUNIT_ASSERT( (bool) ptrRO )
        self.assertTrue(nodeRO.GetAccessMode() == RO)

        nodePRO = Camera.GetNode("PRO")
        # CPPUNIT_ASSERT( (bool) ptrPRO )
        self.assertTrue(nodePRO.GetAccessMode() == RO)

    #       if defined(_MSC_VER) && !defined(PHARLAP_WIN32)
    # http:#rishida.net/tools/conversion/
    def test_UTF16Handling(self):
        pass

    #         wchar_t pBufferUTF16[] = L"\x00E8\x00E9\x00F8\x00DE\x01FD\x043B\x0459\x03A3\x00E6\x010Da\x00DF"
    #         const char pReferenceBufferUTF8[] = {0xC3u, 0xA8u, 0xC3u, 0xA9u, 0xC3u, 0xB8u, 0xC3u, 0x9Eu, 0xC7u, 0xBDu, 0xD0u, 0xBBu,
    #             0xD1u, 0x99u, 0xCEu, 0xA3u, 0xC3u, 0xA6u, 0xE1u, 0x83u, 0x9Au, 0xC3u, 0x9Fu, 0x00u }
    #         # c3 a8 c3 a9 c3 b8 c3 9e c7 bd d0 bb d1 99 ce a3 c3 a6 c4 8d 61 c3 9f
    #         # c3 a8 c3 a9 c3 b8 c3 9e c7 bd d0 bb d1 99 ce a3 c3 a6 e1 83 9a c3 9f
    #         {
    #             gcstring BufferUTF8
    #             BufferUTF8.assign(pBufferUTF16)
    #
    #             const char *pBufferUTF8 = BufferUTF8.c_str()
    #             self.assertEqual( 0, strcmp( pReferenceBufferUTF8, pBufferUTF8 ) )
    #         }
    #
    #         {
    #             gcstring BufferUTF8
    #             BufferUTF8 = pBufferUTF16
    #
    #             const char *pBufferUTF8 = BufferUTF8.c_str()
    #             self.assertEqual( 0, strcmp( pReferenceBufferUTF8, pBufferUTF8 ) )
    #         }
    #
    #         {
    #             gcstring BufferUTF8(pBufferUTF16)
    #
    #             const char *pBufferUTF8 = BufferUTF8.c_str()
    #             self.assertEqual( 0, strcmp( pReferenceBufferUTF8, pBufferUTF8 ) )
    #         }
    #
    #         {
    #             gcstring BufferUTF8
    #             BufferUTF8 = pBufferUTF16
    #
    #             self.assertEqual( 0,  wcscmp( BufferUTF8.w_str().c_str(), pBufferUTF16 ) )
    #         }
    #
    #         {
    #             gcstring BufferUTF8
    #             BufferUTF8 = pBufferUTF16
    #
    #             wostringstream TestStreamUTF16
    #             TestStreamUTF16 << BufferUTF8.w_str().c_str()
    #
    #             wstring &TestStringUTF16 = TestStreamUTF16.str()
    #             wchar_t pBufferUTF16Test[256]
    #             wcscpy( pBufferUTF16Test, TestStringUTF16.c_str() )
    #
    #             self.assertEqual( 0, wcscmp( pBufferUTF16, pBufferUTF16Test) )
    #             self.assertEqual( 0, wcscmp( pBufferUTF16, BufferUTF8.w_str().c_str()) )
    #         }
    #
    #     #ifdef USE_CONSOLE_OUTPUT
    #         # print the register content
    #         {
    #             gcstring BufferUTF8
    #             BufferUTF8.assign(pBufferUTF16)
    #
    #             UINT oldcp = GetConsoleOutputCP()
    #             SetConsoleOutputCP(CP_UTF8)
    #             wprintf(L"%S\n", BufferUTF8.c_str())
    #             SetConsoleOutputCP(oldcp)
    #         }
    #    #endif

    def test_Invalidation(self):
        """[ GenApiTest@StringTestSuite_TestInvalidation.xml|gxml
    
        <Group Comment="Generic">
    
            <String Name="StringA">
                <Visibility>Beginner</Visibility>
                <pIsImplemented>StringA_IsImplemented</pIsImplemented>
                <pIsAvailable>StringA_IsAvailable</pIsAvailable>
                <pIsLocked>StringA_IsLocked</pIsLocked>
                <pValue>StringA_Reg</pValue>
            </String>
            <Integer Name="StringA_IsImplemented">
                <Value>1</Value>
            </Integer>
            <Integer Name="StringA_IsAvailable">
                <Value>1</Value>
            </Integer>
            <Integer Name="StringA_IsLocked">
                <Value>0</Value>
            </Integer>
            <StringReg Name="StringA_Reg">
                <Address>0x10000</Address>
                <Length>16</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Device</pPort>
                <Cachable>WriteThrough</Cachable>
            </StringReg>
            
            <Integer Name="IntegerB">
                <Visibility>Beginner</Visibility>
                <pIsImplemented>IntegerB_IsImplemented</pIsImplemented>
                <pIsAvailable>IntegerB_IsAvailable</pIsAvailable>
                <pIsLocked>IntegerB_IsLocked</pIsLocked>
                <pValue>IntegerB_Reg</pValue>
                <Inc>1</Inc>
                <Representation>Linear</Representation>
            </Integer>
            <Integer Name="IntegerB_IsImplemented">
                <Value>1</Value>
            </Integer>
            <Integer Name="IntegerB_IsAvailable">
                <Value>1</Value>
            </Integer>
            <Integer Name="IntegerB_IsLocked">
                <Value>0</Value>
            </Integer>
            <IntReg Name="IntegerB_Reg">
                <Address>0x10010</Address>
                <Length>4</Length>
                <AccessMode>RO</AccessMode>
                <pPort>Device</pPort>
                <Cachable>WriteAround</Cachable>
                <pInvalidator>CommandC_Reg</pInvalidator>
                <pInvalidator>StringA_Reg</pInvalidator>
                <Endianess>BigEndian</Endianess>
            </IntReg>
    
            <Command Name="CommandC">
                <Visibility>Beginner</Visibility>
                <pIsImplemented>CommandC_IsImplemented</pIsImplemented>
                <pIsAvailable>CommandC_IsAvailable</pIsAvailable>
                <pIsLocked>CommandC_IsLocked</pIsLocked>
                <pValue>CommandC_Reg</pValue>
                <CommandValue>1</CommandValue>
            </Command>
            <Integer Name="CommandC_IsImplemented">
                <Value>1</Value>
            </Integer>
            <Integer Name="CommandC_IsAvailable">
                <Value>1</Value>
            </Integer>
            <Integer Name="CommandC_IsLocked">
                <Value>0</Value>
            </Integer>
            <IntReg Name="CommandC_Reg">
                <Address>0x10014</Address>
                <Length>4</Length>
                <AccessMode>WO</AccessMode>
                <pPort>Device</pPort>
                <Cachable>WriteThrough</Cachable>
                <Endianess>BigEndian</Endianess>
            </IntReg>
    
            <Category Name="Generic">
                <pFeature>StringA</pFeature>
                <pFeature>IntegerB</pFeature>
                <pFeature>CommandC</pFeature>
            </Category>
        </Group>
        <Group Comment="Root">
            <Category Name="Root">
                <pFeature>Generic</pFeature>
            </Category>
        </Group>
        <Port Name="Device">
            <ToolTip>Port giving access to the device.</ToolTip>
        </Port>
    
    
        """

        Port = CTestPort()

        # <StringReg Name = "StringA_Reg">
        # < Address>0x10000 < / Address >
        # < Length>16 < / Length >
        #         char StringA[17] = { 0 }
        #         Port.CreateEntry(0x10000, 16, StringA, RW)

        # <IntReg Name = "IntegerB_Reg">
        # < Address>0x10010 < / Address >
        # < Length>4 < / Length >
        IntegerB = 42
        Port.CreateEntry(0x10010, "uint32_t", IntegerB, RW, LittleEndian)

        # <IntReg Name = "CommandC_Reg">
        # < Address>0x10014 < / Address >
        # < Length>4 < / Length >
        CommandC = 815
        Port.CreateEntry(0x10014, "uint32_t", CommandC, RW, LittleEndian)

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "StringTestSuite_TestInvalidation")
        Camera._Connect(Port, "Device")


# NODE_POINTER(String, StringA)
#         NODE_POINTER(Integer, IntegerB)
#         NODE_POINTER(Command, CommandC)
#     
#         CallbackUtility::Reset()
#         Register(ptrIntegerB.GetNode(), &CallbackUtility::Callback)
#     
#         *ptrStringA = "Bla"
#     
#         self.assertEqual((uint32_t)1, CallbackUtility::Count())
#     
#         ptrCommandC.Execute()
#     
#         self.assertEqual((uint32_t)2, CallbackUtility::Count())

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
