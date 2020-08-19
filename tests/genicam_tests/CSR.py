'''
Created on 04.08.2015

@author: TMoeller
'''

'''
CSR Server
handles access to registers and dispatches read/write requests to handler
routines
Created on 07.05.2012

@author: thies.moeller@baslerweb.com
'''
import genicam


class RMap(object):
    def __init__(self):
        # rmap is a ( addr,len ) -> handler tuple mapping
        self.rmap = {}

    def newReg(self, reg):
        assert self.findRegisters(reg.addr, reg.length) == [], "this address is already defined"
        self.rmap[(reg.addr, reg.length)] = reg

    def findRegisters(self, address, length):
        """
        return a list of registers, that overlap with the map the access pattern
        use an interval tree to handle this with full speed eventually
        """
        sreg = sorted(self.rmap.items(), key=lambda reg: reg[0])
        regs = []
        for key, reg in sreg:
            # overlap from start
            if (address + length) > reg.addr and ((address)
                                                      < (reg.addr + reg.length)):
                regs.append(reg)
            # inside overlap
            elif (address >= reg.addr) and (address < (reg.addr + reg.length)):
                regs.append(reg)
        return regs


class Register(object):
    """
    a register is placed at a given address
    reads/writes referenced with an offset into the register
    calling code has to take care of accessing
    the right portion of the register
    """

    def __init__(self, addr, length, accessmode=genicam.RW):
        self.addr = addr
        self.length = length
        self.accessmode = accessmode

    def read(self, offset, length):
        """
            return length and data ...
        """
        raise NotImplementedError

    def write(self, offset, data):
        raise NotImplementedError


class LocalStorageReg(Register):
    def __init__(self, addr, length, preset=None, accessmode=genicam.RW):
        Register.__init__(self, addr, length, accessmode)
        if preset is None:
            self.data = bytes(length)
        else:
            assert len(preset) == length
            self.data = preset

    def read(self, offset, length=None):
        assert offset < self.length
        assert offset + length <= self.length

        if not genicam.IsReadable(self.accessmode):
            raise genicam.RuntimeException(
                "Register not readable at address 0x%x with length %d" % (self.addr + offset, length), "", 0)

        if length is None:
            return self.data[offset:]
        else:
            return self.data[offset:offset + length]

    def write(self, offset, data):
        assert offset < self.length
        assert offset + len(data) <= self.length

        if not genicam.IsWritable(self.accessmode):
            raise genicam.RuntimeException(
                "Register not writable at address 0x%x with length %d" % (self.addr + offset, len(data)), "", 0)

        self.data = self.data[0:offset] + data + self.data[offset + len(data):]


class CSRServer(object):
    def __init__(self, regmap=None):
        # map from register start to rmap
        self.rmaps = [RMap(), ]
        if regmap is not None:
            self.registerRMap(regmap)

    def registerRMap(self, rmap):
        '''
        register a new address to register mapping
        :param rmap: rmap to register
        '''
        self.rmaps.append(rmap)

    def newReg(self, reg):
        '''
        register a new address to first register map
        :param rmap: rmap to register
        '''
        self.rmaps[0].newReg(reg)

    def read(self, addr, length):
        '''
        is called on a read to a register
        if the access to the register is smaller than the reg width,
        this class handles the read of the relevant bytes
        :param addr: base address of access
        :param length: length of access
        '''
        read_data = bytes()
        read_length = length
        for rmap in self.rmaps:
            regset = rmap.findRegisters(addr, read_length)
            for reg in regset:
                if reg.addr > addr:
                    # fill in space with "0"
                    read_data += bytes(reg.addr - addr)
                    read_length -= (reg.addr - addr)
                    addr += (reg.addr - addr)
                    reg_data = reg.read(0, min(read_length, reg.length))
                    raise genicam.GenericException(
                        "Register not readable at address 0x%x with length %d" % (addr, length), "", 0)
                else:
                    # offset into register
                    reg_offs = addr - reg.addr
                    reg_data = reg.read(
                        reg_offs, min(read_length, reg.length - reg_offs))

                read_data += reg_data
                addr += len(reg_data)
                read_length -= len(reg_data)
        # fill up rest
        if length - len(read_data) > 0:
            read_data += bytes(length - len(read_data))
            raise genicam.GenericException("Register not readable at address 0x%x with length %d" % (addr, length), "",
                                           0)
        return read_data

    def write(self, addr, data):
        '''
        is called on a write to a register
        if the write is misaligned, this method handles the read modify write of
        the underlying registers
        :param addr: base address of access
        :param length: length of acces
        '''
        length = len(data)
        for rmap in self.rmaps:
            regset = rmap.findRegisters(addr, length)
            if not regset:
                raise genicam.GenericException(
                        "There is no register at address 0x%x with length %d" % (addr, length), "", 0)

            for reg in regset:
                if addr < reg.addr:
                    # cut access
                    data = data[reg.addr - addr:]
                    addr = reg.addr
                    reg_offs = 0
                    # the address is too low
                    raise genicam.GenericException(
                        "Register not writable at address 0x%x with length %d Too Low" % (addr, length), "", 0)
                elif addr >= reg.addr:
                    reg_offs = addr - reg.addr

                write_len = min(length, reg.length - reg_offs)
                reg.write(reg_offs, data[:write_len])
                if write_len < len(data):
                    raise genicam.GenericException(
                        "Register not writable at address 0x%x with length %d" % (addr, length), "", 0)


if __name__ == '__main__':
    def pad(string, length, padding="\0".encode()):
        if len(string) < length:
            return string + padding * (length - len(string))
        else:
            return string


    Basler = RMap()

    R1 = LocalStorageReg(4, 4, "AAAA".encode())
    R2 = LocalStorageReg(8, 4, "BBBB".encode())
    R3 = LocalStorageReg(12, 4, "CCCC".encode())
    R4 = LocalStorageReg(20, 4, "DDDD".encode())

    R5 = LocalStorageReg(0x1000, 11, "Hello World".encode())

    Basler.newReg(R1)
    Basler.newReg(R2)
    Basler.newReg(R3)
    Basler.newReg(R4)
    Basler.newReg(R5)
    csr = CSRServer(Basler)

    assert csr.read(0, 4) == "\0\0\0\0".encode()
    assert csr.read(4, 4) == "AAAA".encode()
    assert csr.read(8, 4) == "BBBB".encode()
    assert csr.read(12, 4) == "CCCC".encode()
    assert csr.read(16, 4) == "\0\0\0\0".encode()
    assert csr.read(20, 4) == "DDDD".encode()

    assert csr.read(0, 8) == "\0\0\0\0AAAA".encode()
    assert csr.read(4, 4) == "AAAA".encode()
    assert csr.read(6, 4) == "AABB".encode()
    assert csr.read(4, 12) == "AAAABBBBCCCC".encode()
    assert csr.read(0, 24) == "\0\0\0\0AAAABBBBCCCC\0\0\0\0DDDD".encode()

    csr.write(0, "12345678901234567890SSSS".encode())
    assert R1.data == b'5678'
    assert R2.data == b'9012'
    assert R3.data == b'3456'
    assert R4.data == b'SSSS'

    assert csr.read(0x1000, 32) == ("Hello World" + "\0" * (32 - 11)).encode()

    print("ok")
