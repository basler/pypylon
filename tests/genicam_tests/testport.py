'''
Created on 03.08.2015

@author: TMoeller
'''
import functools

# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:  Fritz Dierks
#  $Header$
# -----------------------------------------------------------------------------
"""!
\file
"""
import genicam
import struct
import CSR


def type_map(dtype):
    if dtype.startswith("str"):
        return dtype[3:] + "s"
    else:
        mapping = {
            "float32_t": "f",
            "float64_t": "d",
            "int16_t": "h",
            "int32_t": "i",
            "int64_t": "q",
            "int8_t": "b",
            "uint16_t": "H",
            "uint32_t": "I",
            "uint64_t": "Q",
            "uint8_t": "B",
        }
        return mapping[dtype]


def cast_buffer(dtype, endianess, val):
    # decode a buffer according to given dtype and endianess
    prefix = {genicam.LittleEndian: "<",
              genicam.BigEndian: ">"}[endianess]

    return struct.unpack(prefix + type_map(dtype), val)[0]


def cast_data(dtype, endianess, val):
    # decode a buffer according to given dtype and endianess
    prefix = {genicam.LittleEndian: "<",
              genicam.BigEndian: ">"}[endianess]
    return struct.pack(prefix + type_map(dtype), val)


def sizeof(dtype):
    if dtype.startswith("str"):
        return int(dtype[3:])
    else:
        return struct.calcsize(type_map(dtype))


class StructEntry(object):
    def __init__(self, dtype, endianess):
        self.dtype = dtype
        self.endianess = endianess
        self.value = None

    def getsize(self):
        return len(cast_data(self.dtype, self.endianess, 42))

    def SetValue(self, val):
        self.value = val

    def GetValue(self):
        return self.value


class CTestPort(genicam.CPortImpl):
    """
    genicam device port implementation
    """

    def __init__(self):
        genicam.CPortImpl.__init__(self)
        self.isOpen = True
        self.csr = CSR.CSRServer()

    def Read(self, address, length):
        return self.csr.read(address, length)

    def Write(self, address, data):
        self.csr.write(address, data)

    def GetAccessMode(self):
        if self.isOpen:
            return genicam.RW
        else:
            return genicam.NA

    def Open(self):
        self.isOpen = True

    def Close(self):
        self.isOpen = False

    def CreateEntry(self, addr, dtype, value, accessmode, endianess):

        if dtype.startswith("str"):
            data = value.encode("utf-8")
        elif dtype == "raw":
            data = value
        else:
            data = cast_data(dtype, endianess, value)
        reg = CSR.LocalStorageReg(addr, len(data), data, accessmode)
        self.csr.newReg(reg)
        return reg

    # -> value, accessmode
    def LookupEntry(self, addr, dtype):
        raise NotImplementedError

    def UpdateEntry(self, addr, data, accessmode):
        res = self.csr.rmaps[0].findRegisters(addr, len(data))
        assert len(res) == 1
        assert res[0].addr == addr
        assert res[0].length == len(data)
        res[0].accessmode = accessmode
        res[0].data = data

    def Replay(self, **args):
        raise NotImplementedError

    def ShowMap(self):
        for rm in self.csr.rmaps:
            for r in rm.rmap:
                print(r)


class CQuadTestPort(CTestPort):
    def __init__(self):
        super(CQuadTestPort, self).__init__()

    def CreateEntries(self, StartAdr, EndAdr, dtype, buffer, AccessMode, endianess):
        raise NotImplementedError

    def Read(self, address, length):
        raise NotImplementedError

    def Write(self, address, data):
        raise NotImplementedError


# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def testBit(int_type, offset):
    mask = 1 << offset
    return (int_type & mask) != 0


# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset, val):
    mask = (val & 1) << offset
    return (int_type | mask)


# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)


class CStructTestPort(CTestPort):
    __initialized = False

    def _setData(self, reg, dtype, endianess, value):
        reg.data = cast_data(dtype, endianess, value)

    def _getData(self, reg, dtype, endianess):
        return cast_buffer(dtype, endianess, reg.data)

    def _setBitInReg(self, reg, dtype, endianess, pos, val):
        val = self._getData(reg, dtype, endianess)
        newval = setBit(clearBit(val, pos), pos, val)
        self._setData(reg, dtype, endianess, newval)

    def _getBitInReg(self, reg, dtype, endianess, pos):
        val = self._getData(reg, dtype, endianess)
        return testBit(val, pos)

    def __init__(self, reg_set, BaseAddress=0):
        super(CStructTestPort, self).__init__()

        self.struct_entries = {}
        self.m_BaseAddress = BaseAddress
        offs = 0
        for v in reg_set:
            k, dtype, preset, access, endianess = v
            if ",bits" in dtype:
                # create one instance of the register
                dtype = dtype.split(",")[0]
                reg = self.CreateEntry(BaseAddress + offs, dtype, preset, access, endianess)

                bitsInReg = sizeof(dtype) * 8
                for b in range(bitsInReg):
                    if endianess == genicam.BigEndian:
                        self.struct_entries["bit%d" % b] = (reg,
                                                            functools.partial(self._getBitInReg, reg, dtype, endianess,
                                                                              bitsInReg - b - 1),
                                                            functools.partial(self._setBitInReg, reg, dtype, endianess,
                                                                              bitsInReg - b - 1),
                                                            )
                    else:
                        self.struct_entries["bit%d" % b] = (reg,
                                                            functools.partial(self._getBitInReg, reg, dtype, endianess,
                                                                              b),
                                                            functools.partial(self._setBitInReg, reg, dtype, endianess,
                                                                              b),
                                                            )


            else:
                reg = self.CreateEntry(BaseAddress + offs, dtype, preset, access, endianess)
                self.struct_entries[k] = (reg,
                                          functools.partial(self._getData, reg, dtype, endianess),
                                          functools.partial(self._setData, reg, dtype, endianess),
                                          )
            offs += sizeof(dtype)

        self.ResetStatistics()
        self.__initialized = True

    def GetPrincipalInterfaceType(self):
        return genicam.intfIPort

    def ResetStatistics(self):
        self.m_NumReads = 0
        self.m_NumWrites = 0

    def GetNumReads(self):
        return self.m_NumReads

    def GetNumWrites(self):
        return self.m_NumWrites

    def Read(self, address, length):
        self.m_NumReads += 1
        return super(CStructTestPort, self).Read(address, length)

    def Write(self, address, data):
        self.m_NumWrites += 1
        return super(CStructTestPort, self).Write(address, data)

    def __getattr__(self, name):
        if self.__initialized and name in self.struct_entries:
            reg, read, write = self.struct_entries[name]
            return read()
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if self.__initialized and name in self.struct_entries:
            reg, read, write = self.struct_entries[name]
            write(value)
        else:
            object.__setattr__(self, name, value)


if __name__ == '__main__':
    Port = CTestPort()
    Port.CreateEntry(0x0104, "uint32_t", 1024, genicam.RW, genicam.LittleEndian)
    Port.CreateEntry(0x0108, "uint32_t", 1024, genicam.RW, genicam.LittleEndian)
    Port.CreateEntry(0x0110, "str16", "*" * 16, genicam.RW, genicam.LittleEndian)

    Port.Write(0x0110, "1234".encode())
    print(Port.Read(0x0110, 5))

    regs = [("Gain", "uint32_t", 0, genicam.RW, genicam.LittleEndian),
            ("GainAutoReg", "uint8_t", 22, genicam.RO, genicam.LittleEndian)
            ]

    ab = CStructTestPort(regs)

    ab.Gain = 42
    print(ab.GainAutoReg)
    ab.GainAutoReg = 12

    print(ab.Gain)
    ab.ShowMap()
