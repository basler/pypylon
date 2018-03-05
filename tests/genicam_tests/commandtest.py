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
from testport import CTestPort, cast_buffer, cast_data, sizeof, CStructTestPort
from callbackhelper import CallbackObject


class CommandTestSuite(GenicamTestCase):
    def test_Command01(self):
        """[ GenApiTest@CommandTestSuite_TestCommand01.xml|gxml
    
        <Category Name="Root">
           <pFeature>command</pFeature>
        </Category>
    
        <Command Name="command">
           <pValue>myIntReg</pValue>
           <CommandValue>0x4321</CommandValue>
        </Command>
    
        <IntReg Name="myIntReg">
            <Address>0x00ff</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>MyPort</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Port Name="MyPort"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand01")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x00ff, "uint32_t", 42, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        #
        # Test the ICommand interface
        #

        # retrieve the node and convert it to ICommand
        Node = Camera.GetNode("command")
        Cmd = Node
        self.assertTrue(bool(Node))
        self.assertTrue(bool(Cmd))
        self.assertEqual(intfICommand, Cmd.GetNode().GetPrincipalInterfaceType())

        ##### getproperty of command pointer -
        try:
            ValueStr, AttributeStr = Cmd.GetNode().GetProperty("CommandValue")
        except:
            pass

        # execute function
        Cmd.Execute()
        # is executing?
        self.assertEqual(False, Cmd.IsDone())
        # manipulate the command register in order to simulate a self-resetting toggle
        # CLittleEndian<int32_t> tmp
        tmp_data = Port.Read(0x00ff, sizeof("int32_t"))
        self.assertEqual(0x21430000, cast_buffer("int32_t", LittleEndian, tmp_data))
        tmp = 0
        Port.Write(0x00ff, cast_data("int32_t", LittleEndian, tmp))
        self.assertEqual(True, Cmd.IsDone())

        # once again with verification
        Cmd.Execute()
        self.assertEqual(False, Cmd.IsDone(True))
        Port.Write(0x00ff, cast_data("int32_t", LittleEndian, tmp))
        self.assertEqual(True, Cmd.IsDone(True))

        # happy path (what to test on execution without verification?)
        Cmd.Execute(False)

        # execute function
        Cmd()
        # is executing?
        self.assertEqual(False, Cmd.IsDone())
        # manipulate the command register in order to simulate a self-resetting toggle
        tmp_data = Port.Read(0x00ff, sizeof("int32_t"))
        self.assertEqual(0x21430000, cast_buffer("int32_t", LittleEndian, tmp_data))
        tmp = 0
        Port.Write(0x00ff, cast_data("int32_t", LittleEndian, tmp))
        self.assertEqual(True, Cmd.IsDone())

        # TestAccessMode
        self.assertEqual(RW, Cmd.GetAccessMode())

        #
        # Test the IValue interface
        #
        Value = Cmd
        strExec = "0"
        # function is done => value is "0"
        self.assertEqual(strExec, Value.ToString())
        # execute using a string
        strExec = "1"
        Value.FromString(strExec)
        # function is executing => value is "1"
        self.assertEqual(strExec, Value.ToString())
        self.assertTrue(None != Value.GetNode())

        # try to use an illegal string
        with self.assertRaises(InvalidArgumentException):
            Value.FromString("foo")

        Value.FromString("true")

    def test_Command02(self):
        """[ GenApiTest@CommandTestSuite_TestCommand02.xml|gxml
    
        <Command Name="command">
            <Value>0</Value>
            <CommandValue>1</CommandValue>
        </Command>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand02")

        #
        # Test the ICommand interface
        #

        # retrieve the node and convert it to ICommand
        Node = Camera.GetNode("command")
        Cmd = Node
        self.assertTrue(bool(Node))
        self.assertTrue(bool(Cmd))

        #
        # Test the IValue interface
        #
        # Execute function
        Value = Cmd
        strExec = "0"
        # Function not executing => CommandValue is 0
        self.assertEqual(strExec, Value.ToString())

        # Execute function
        # 1st Method
        strExec = "0"
        with self.assertRaises(InvalidArgumentException):
            Value.FromString(strExec)

        # 2nd Method
        strExec = "1"
        Value.FromString(strExec)  # equivalent to "ptrCmd.Execute()"

        # Function not executing (a floating command is immediatelx ready )
        strExec = "0"
        self.assertEqual(strExec, Value.ToString())

        # is executing?
        self.assertEqual(True, Cmd.IsDone())

    def test_Command03(self):
        """[ GenApiTest@CommandTestSuite_TestCommand03.xml|gxml
    
        <Command Name="Command">
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand03")

        Command = Camera.GetNode("Command")
        self.assertTrue(bool(Command))

        Value = Camera.GetNode("Value")
        self.assertTrue(bool(Value))

        CommandValue = Camera.GetNode("CommandValue")
        self.assertTrue(bool(CommandValue))

        CallbackTarget = CallbackObject()
        Register(Command.GetNode(), CallbackTarget.Callback)

        # nothing happened so no callback expected
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(0, CallbackTarget.Count())

        # a first callback happens after execute
        Command.Execute()
        self.assertEqual(1, CallbackTarget.Count())

        for count in range(10, 0):
            # no callback on IsDone because the value has not changed yet
            self.assertEqual(False, Command.IsDone())
            # self.assertEqual( (int64_t)42, ptrValue.GetValue() )
            # self.assertEqual( 1, CallbackTarget.Count() )

        # now the value has changed so we expect a callback
        Value.SetValue(0)
        self.assertEqual(2, CallbackTarget.Count())

        # On IsDone the Command node notives that the vale has changed and fires another time
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(3, CallbackTarget.Count())

    def test_Command04(self):
        """[ GenApiTest@CommandTestSuite_TestCommand04.xml|gxml
    
        <Command Name="Command">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand04")

        Command = Camera.GetNode("Command")
        self.assertTrue(bool(Command))

        Value = Camera.GetNode("Value")
        self.assertTrue(bool(Value))

        CommandValue = Camera.GetNode("CommandValue")
        self.assertTrue(bool(CommandValue))

        CallbackTarget = CallbackObject()
        Register(Command.GetNode(), CallbackTarget.Callback)

        # due to the execute a callback is fired
        Command.Execute()
        self.assertEqual(1, CallbackTarget.Count())

        # since the command node is WO IsDone does not trigger a callback
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(1, CallbackTarget.Count())

    def test_Command05(self):
        """[ GenApiTest@CommandTestSuite_TestCommand05.xml|gxml
    
        <Command Name="Command">
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
            <PollingTime>1000</PollingTime>
        </Command>
    
        <Integer Name="CommandValue">
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        <Command Name="CommandWO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
            <PollingTime>1000</PollingTime>
        </Command>
    
        <Command Name="Command_ValueWO">
            <pValue>ValueWO</pValue>
            <pCommandValue>CommandValue</pCommandValue>
            <PollingTime>1000</PollingTime>
        </Command>
    
        <Integer Name="ValueWO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand05")

        Command = Camera.GetNode("Command")
        self.assertTrue(bool(Command))

        Value = Camera.GetNode("Value")
        self.assertTrue(bool(Value))

        CommandValue = Camera.GetNode("CommandValue")
        self.assertTrue(bool(CommandValue))

        CallbackTarget = CallbackObject()
        Register(Command.GetNode(), CallbackTarget.Callback)

        Command.Execute()
        self.assertEqual(1, CallbackTarget.Count())
        self.assertEqual(False, Command.IsDone())

        Camera._Poll(500)
        self.assertEqual(1, CallbackTarget.Count())
        self.assertEqual(False, Command.IsDone())

        Camera._Poll(500)
        self.assertEqual(2, CallbackTarget.Count())
        self.assertEqual(False, Command.IsDone())

        # now the self-clearing flag is clearing
        Value.SetValue(0)
        # this is due to the fact that Command is dependent on value
        self.assertEqual(3, CallbackTarget.Count())

        Camera._Poll(1000)
        self.assertEqual(4, CallbackTarget.Count())
        self.assertEqual(True, Command.IsDone())

        # similar tests with WO node (done immediatelly, no polling)
        CommandWO = Camera.GetNode("CommandWO")
        self.assertTrue(bool(CommandWO))

        CallbackTargetWO = CallbackObject()
        Register(CommandWO.GetNode(), CallbackTargetWO.Callback)

        CommandWO.Execute()
        self.assertEqual(1, CallbackTargetWO.Count())
        self.assertEqual(True, CommandWO.IsDone())

        Camera._Poll(1000)
        self.assertEqual(1, CallbackTargetWO.Count())
        self.assertEqual(True, CommandWO.IsDone())

        # and again with command having a WO value
        Command_ValueWO = Camera.GetNode("Command_ValueWO")
        self.assertTrue(bool(Command_ValueWO))

        CallbackTarget_ValueWO = CallbackObject()
        Register(Command_ValueWO.GetNode(), CallbackTarget_ValueWO.Callback)

        Command_ValueWO.Execute()
        self.assertEqual(1, CallbackTarget_ValueWO.Count())
        self.assertEqual(True, Command_ValueWO.IsDone())

        Camera._Poll(1000)
        self.assertEqual(1, CallbackTarget_ValueWO.Count())
        self.assertEqual(True, Command_ValueWO.IsDone())

    def test_Command06(self):
        """[ GenApiTest@CommandTestSuite_TestCommand06.xml|gxml
    
        <Command Name="Command">
            <pIsLocked>LockIt</pIsLocked>
            <ImposedAccessMode>WO</ImposedAccessMode>
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
            <pIsImplemented>CommandValueIsImpl</pIsImplemented>
            <pIsAvailable>CommandValueIsAvail</pIsAvailable>
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="LockIt">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="CommandValueIsAvail">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="CommandValueIsImpl">
            <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand06")

        Command = Camera.GetNode("Command")

        self.assertEqual(NA, Command.GetAccessMode())

        with self.assertRaises(AccessException):
            Command.FromString("42")
        with self.assertRaises(AccessException):
            Command.Execute()

        # disable the command value
        CmdValueAvailability = Camera.GetNode("CommandValueIsAvail")
        LockCommand = Camera.GetNode("LockIt")
        LockCommand.SetValue(0)
        CmdValueAvailability.SetValue(0)
        self.assertEqual(NA, Command.GetAccessMode())
        with self.assertRaises(AccessException):
            Command.FromString("42")
        with self.assertRaises(AccessException):
            Command.Execute()

        CmdValueImpl = Camera.GetNode("CommandValueIsImpl")
        CmdValueImpl.SetValue(0)
        self.assertEqual(NI, Command.GetAccessMode())

    def test_Command07(self):
        """[ GenApiTest@CommandTestSuite_TestCommand07.xml|gxml
    
            <Command Name="CommandRO">
                <ImposedAccessMode>RO</ImposedAccessMode>
                <pValue>Value</pValue>
                <CommandValue>1</CommandValue>
            </Command>
    
            <Command Name="Command_ValueWO">
                <pValue>Value</pValue>
                <pCommandValue>CommandValueWO</pCommandValue>
            </Command>
    
            <Integer Name="CommandValueWO">
                <ImposedAccessMode>WO</ImposedAccessMode>
                <Value>42</Value>
            </Integer>
    
            <Integer Name="Value">
                <Value>0</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommand07")

        CommandRO = Camera.GetNode("CommandRO")
        self.assertTrue(bool(CommandRO))
        Command_ValueWO = Camera.GetNode("Command_ValueWO")
        self.assertTrue(bool(Command_ValueWO))

        with self.assertRaises(AccessException):
            CommandRO.Execute()
        with self.assertRaises(AccessException):
            Command_ValueWO.Execute()

    def test_CommandMantis250(self):
        """[ GenApiTest@CommandTestSuite_TestCommandMantis250.xml|gxml
    
        <Integer Name="BinningVertical">
          <pValue>VerticalBinningReg</pValue>
          <Representation>Linear</Representation>
        </Integer>
    
        <IntReg Name="VerticalBinningReg">
          <Address>0x4</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <pInvalidator>UserSetLoadReg</pInvalidator>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Command Name="Command">
          <pValue>UserSetLoadReg</pValue>
          <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
          <Value>42</Value>
        </Integer>
    
        <IntReg Name="UserSetLoadReg">
          <Address>0x8</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Cachable>NoCache</Cachable>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Port Name="MyPort"/>
    
        """
        Camera = CNodeMapRef()

        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommandMantis250")

        Port = CTestPort()
        Port.CreateEntry(0x0004, "uint32_t", 2, RW, BigEndian)  # VerticalBinningReg
        Port.CreateEntry(0x0008, "uint64_t", 0, RW, BigEndian)  # UserSetLoadReg

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Command = Camera.GetNode("Command")

        Binning = Camera.GetNode("BinningVertical")

        CallbackBinning = CallbackObjectMantis250()
        Register(Binning.GetNode(), CallbackBinning.Callback)

        CallbackCommand = CallbackObjectMantis250()
        Register(Command.GetNode(), CallbackCommand.Callback)

        # this writes 42 to the UserSetLoadReg
        # because VerticalBinningReg has a pInvalidates pointer to UserSetLoadReg it is invalidated
        Command.Execute()
        self.assertEqual(1, CallbackCommand.Count())
        self.assertEqual(1, CallbackBinning.Count())

        # since UserSetLoadReg has not change no callback fires on IsDone
        self.assertEqual(False, Command.IsDone())
        self.assertEqual(1, CallbackBinning.Count())
        self.assertEqual(1, CallbackCommand.Count())

        # now we reset UserSetLoadReg
        value = 0
        AccessMode = RO
        Port.UpdateEntry(0x0008, cast_data("uint64_t", LittleEndian, value), AccessMode)

        # on the next IsDone the callback fires
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(2, CallbackCommand.Count())
        self.assertEqual(2, CallbackBinning.Count())

    def test_CommandMantis257(self):
        """[ GenApiTest@CommandTestSuite_TestCommandMantis257.xml|gxml
    
        <Command Name="Command">
            <pValue>Value</pValue>
            <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommandMantis257")

        Command = Camera.GetNode("Command")

        Value = Camera.GetNode("Value")

        CommandValue = Camera.GetNode("CommandValue")

        CallbackTarget = CallbackObjectMantis257()
        Register(Command.GetNode(), CallbackTarget.Callback)

        # due to the execute a callback is fired
        Command.Execute()
        self.assertEqual(1, CallbackTarget.Count())
        self.assertEqual(False, CallbackTarget.NodeError())

        # due to changing the value another callback fires
        # BEWARE: inside the callback function (see CallbackObjectMantis257 class)
        # there is a call to IsDone. Since the cale has changed to
        # zero the command is now done and another callback fires
        Value.SetValue(0)
        self.assertEqual(3, CallbackTarget.Count())

        # since we have already called IsDone once no additional callback is fired.
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(3, CallbackTarget.Count())

    # modification of TestCommandMantis250, where the pInvalidator points directly to the command node
    # the depending features should get updated twice per command as well
    def test_CommandMantis250_sch11(self):
        # <pInvalidator> pointing to a non-register node
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@CommandTestSuite_TestCommandMantis250_sch11.xml|gxml
        <Integer Name="BinningVertical">
          <pValue>pVerticalBinningReg</pValue>
          <Representation>Linear</Representation>
        </Integer>
        <IntReg Name="pVerticalBinningReg">
          <Address>0x4</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <pInvalidator>Command</pInvalidator>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Command Name="Command">
            <pValue>pUserSetLoadReg</pValue>
            <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="CommandValue">
            <Value>42</Value>
        </Integer>
    
        <IntReg Name="pUserSetLoadReg">
          <Address>0x8</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Cachable>NoCache</Cachable>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Port Name="MyPort"/>
    
        """
        Camera = CNodeMapRef()

        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommandMantis250_sch11")

        Port = CTestPort()
        Port.CreateEntry(0x0004, "uint32_t", 2, RW, BigEndian)
        Port.CreateEntry(0x0008, "uint64_t", 0, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Command = Camera.GetNode("Command")

        Binning = Camera.GetNode("BinningVertical")

        CallbackBinning = CallbackObjectMantis250()
        Register(Binning.GetNode(), CallbackBinning.Callback)

        CallbackCommand = CallbackObjectMantis250()
        Register(Command.GetNode(), CallbackCommand.Callback)

        Command.Execute()
        self.assertEqual(1, CallbackBinning.Count())

        self.assertEqual(False, Command.IsDone())
        self.assertEqual(False, Command.IsDone(False))
        self.assertEqual(1, CallbackBinning.Count())
        self.assertEqual(1, CallbackCommand.Count())

        value = 0
        AccessMode = RO
        Port.UpdateEntry(0x0008, cast_data("uint64_t", LittleEndian, value), AccessMode)

        self.assertEqual(True, Command.IsDone(False))
        self.assertEqual(True, Command.IsDone())
        self.assertEqual(2, CallbackCommand.Count())
        self.assertEqual(2, CallbackBinning.Count())

    def test_CornerCases(self):
        """[ GenApiTest@CommandTestSuite_TestCornerCases.xml|gxml
    
        <Command Name="CommandValWO">
            <pValue>Value</pValue>
            <pCommandValue>CommandValueWO</pCommandValue>
        </Command>
    
        <Integer Name="CommandValueWO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Value">
            <Value>0</Value>
        </Integer>
    
        <Command Name="CommandValNI">
            <pValue>Value</pValue>
            <pCommandValue>CommandValueNI</pCommandValue>
        </Command>
    
        <Integer Name="CommandValueNI">
            <pIsImplemented>Zero</pIsImplemented>
            <Value>42</Value>
        </Integer>
    
        <Integer Name="Zero">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCornerCases")

        # test command which does not have readable command value
        CommandValWO = Camera.GetNode("CommandValWO")
        self.assertTrue(bool(CommandValWO))
        with self.assertRaises(AccessException):
            CommandValWO.Execute()
        # ??self.assertRaises (ptrCommandValWO.IsDone(), AccessException)
        self.assertEqual(NA, CommandValWO.GetAccessMode())

        # test command which has command value NI
        CommandValNI = Camera.GetNode("CommandValNI")
        self.assertTrue(bool(CommandValNI))
        with self.assertRaises(AccessException):
            CommandValNI.Execute()
        self.assertEqual(NI, CommandValNI.GetAccessMode())
        with self.assertRaises(AccessException):
            CommandValNI.IsDone()

    def test_CommandCaching(self):
        """[ GenApiTest@CommandTestSuite_TestCommandCaching.xml|gxml
    
        <Command Name="Command">
           <pValue>Value</pValue>
           <pCommandValue>CommandValue</pCommandValue>
        </Command>
    
        <Integer Name="Value">
           <Value>0</Value>
        </Integer>
    
        <IntReg Name="CommandValue">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Device</pPort>
            <pInvalidator>Value</pInvalidator>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Device"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestCommandCaching")

        regs = [("ValueCommand", "uint32_t", 0, RW, LittleEndian),
                ]

        Port = CStructTestPort(regs)
        Camera._Connect(Port, "Device")

        Command = Camera.GetNode("Command")

        Value = Camera.GetNode("Value")

        Port.ValueCommand = 1
        Command.Execute()
        self.assertEqual(1, Value.GetValue())

        Port.ValueCommand = 2
        Command.Execute()
        self.assertEqual(2, Value.GetValue())

    def test_Ticket768(self):
        """[ GenApiTest@CommandTestSuite_TestTicket768.xml|gxml
    
        <Command Name="MyCommand1">
           <pValue>ValueReg1</pValue>
           <CommandValue>1</CommandValue>
        </Command>
    
        <IntReg Name="ValueReg1">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Device</pPort>
            <Cachable>NoCache</Cachable>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Command Name="MyCommand2">
           <pValue>ValueReg2</pValue>
           <CommandValue>1</CommandValue>
        </Command>
    
        <IntReg Name="ValueReg2">
            <Address>0x0004</Address>
            <Length>4</Length>
            <AccessMode>WO</AccessMode>
            <pPort>Device</pPort>
            <Cachable>NoCache</Cachable>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Command Name="MyCommand3">
           <ImposedAccessMode>WO</ImposedAccessMode>
           <pValue>ValueReg3</pValue>
           <CommandValue>1</CommandValue>
        </Command>
    
        <IntReg Name="ValueReg3">
            <Address>0x0008</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Device</pPort>
            <Cachable>NoCache</Cachable>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Device"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CommandTestSuite_TestTicket768")

        regs = [("ValueCommand1", "uint32_t", 0, RW, LittleEndian),
                ("ValueCommand2", "uint32_t", 0, RW, LittleEndian),
                ("ValueCommand3", "uint32_t", 0, RW, LittleEndian), ]

        Port = CStructTestPort(regs)
        Camera._Connect(Port, "Device")

        print("1) RW Value\n")

        MyCommand1 = Camera.GetNode("MyCommand1")
        Port.ValueCommand1 = 0
        Port.ResetStatistics()
        print("Reset   : NumReads= ", Port.GetNumReads(), "\n")

        print("Execute!\n")
        MyCommand1.Execute()
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(0, Port.GetNumReads())

        print("IsDone?\n")
        self.assertEqual(False, MyCommand1.IsDone())
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(1, Port.GetNumReads())

        print("Done!\n")
        Port.ValueCommand1 = 0

        print("IsDone?\n")
        self.assertEqual(True, MyCommand1.IsDone())
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(2, Port.GetNumReads())

        print("2) WO Value\n")

        MyCommand2 = Camera.GetNode("MyCommand2")
        Port.ValueCommand2 = 0
        Port.ResetStatistics()
        print("Reset   : NumReads= ", Port.GetNumReads(), "\n")

        print("Execute!\n")
        MyCommand2.Execute()
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(0, Port.GetNumReads())

        print("IsDone?\n")
        self.assertEqual(True, MyCommand2.IsDone())
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(0, Port.GetNumReads())

        print("3) Imposed WO on the Command\n")

        MyCommand3 = Camera.GetNode("MyCommand3")
        Port.ValueCommand3 = 0
        Port.ResetStatistics()
        print("Reset   : NumReads= ", Port.GetNumReads(), "\n")

        print("Execute!\n")
        MyCommand3.Execute()
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(0, Port.GetNumReads())

        print("IsDone?\n")
        self.assertEqual(True, MyCommand3.IsDone())
        print("NumReads= ", Port.GetNumReads(), "\n")
        self.assertEqual(0, Port.GetNumReads())


# Local CallbackObject for testing Mantis Bug #250
class CallbackObjectMantis250(object):
    m_Count = 0

    def Reset(self):
        self.m_Count = 0

    def Count(self):
        return self.m_Count

    def Callback(self, Node):
        self.m_Count += 1


# Local CallbackObject for testing Mantis Bug #257
class CallbackObjectMantis257(object):
    def __init__(self):
        self.m_Count = 0
        self.m_NodeError = False

    def Reset(self):
        self.m_Count = 0

    def Count(self):
        return self.m_Count

    def NodeError(self):
        return self.m_NodeError

    def Callback(self, Node):
        self.m_Count += 1
        if (self.m_Count > 3):
            return
        Command = Node
        if (Command):
            Command.IsDone()
        else:
            self.m_NodeError = True


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
