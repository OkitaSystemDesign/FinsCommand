from datetime import datetime
from socket import *
import struct
import time
from .errors import FinsResponseError

BUFSIZE = 4096

class fins:
    addr = ()
    destfins = []
    srcfins = []
    

    def __init__(self, host, destfinsadr="0.0.0", srcfinsadr="0.127.0", timeout=2.0):
        self.addr = (host, 9600)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.settimeout(timeout)
        
        self.destfins = destfinsadr.split('.')
        if destfinsadr=="0.0.0":
            self.hostadr = host.split('.')
            self.destfins[1] = self.hostadr[3]

        self.srcfins = srcfinsadr.split('.')

    def offset(self, adr, offset):
        mtype = adr[:1]
        moffset =[]
        if mtype == 'D':
            mtype = 0x82
            moffset = list((int(adr[1:])+offset).to_bytes(2,'big'))
        elif mtype == 'E':
            bank = int(adr[1:2], 16)
            mtype = 0xA0 + bank
            moffset = list((int(adr[3:])+offset).to_bytes(2,'big'))
        elif mtype.isdigit():
            mtype = 0xB0
            moffset = list((int(adr)+offset).to_bytes(2,'big'))
        elif mtype == 'W':
            mtype = 0xB1
            moffset = list((int(adr[1:])+offset).to_bytes(2,'big'))
        elif mtype == 'H':
            mtype = 0xB2
            moffset = list((int(adr[1:])+offset).to_bytes(2,'big'))
        
        return mtype, moffset

    # Fins Header
    def finsheader(self):
        ary = bytearray(10)
        ary[0] = 0x80
        ary[1] = 0x00
        ary[2] = 0x02
        ary[3] = int(self.destfins[0])      # Destination NetNo
        ary[4] = int(self.destfins[1])      # Destination NodeNo
        ary[5] = int(self.destfins[2])      # Destination UnitNo
        ary[6] = int(self.srcfins[0])       # Source NetNo
        ary[7] = int(self.srcfins[1])       # Source NodeNo
        ary[8] = int(self.srcfins[2])       # Source UnitNo
        ary[9] = 0x00                       # SID

        return ary

    # Memory area read
    def read(self, memaddr, readsize):
        readnum = readsize // 990
        remainder = readsize % 990

        data = bytes()
        for cnt in range(readnum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == readnum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
                
            finsary = bytearray(8)
            finsary[0] = 0x01
            finsary[1] = 0x01
            finsary[2] = memtype
            finsary[3] = memoffset[0]
            finsary[4] = memoffset[1]
            finsary[5] = 0x00
            finsary[6] = rsize[0]
            finsary[7] = rsize[1]

            rcv = self.SendCommand(finsary)

            data += rcv[14:]
        
        return data
            
    # Memory area write
    def write(self, memaddr, writedata):
        if len(writedata) % 2 == 1:
            return
        writeWordSize = len(writedata) // 2

        writenum = writeWordSize // 990
        remainder = writeWordSize % 990

        finsres = bytes()
        for cnt in range(writenum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == writenum:
                size = remainder
            else:
                size = 990
                
            rsize = list(int(size).to_bytes(2,'big'))
            finsary = bytearray(8 + size * 2)

            finsary[0] = 0x01
            finsary[1] = 0x02
            finsary[2] = memtype
            finsary[3] = memoffset[0]
            finsary[4] = memoffset[1]
            finsary[5] = 0x00
            finsary[6] = rsize[0]
            finsary[7] = rsize[1]
            pos = cnt * 990 * 2
            finsary[8:] = writedata[pos: pos + size * 2]

            rcv = self.SendCommand(finsary)

        finsres = rcv[10:]

        return finsres

    # Memory area fill
    def fill(self, memaddr, size, writedata):
        memtype, memoffset = self.offset(memaddr, 0)
        
        finsary = bytearray(10)
        finsary[0] = 0x01
        finsary[1] = 0x03
        finsary[2] = memtype
        finsary[3] = memoffset[0]
        finsary[4] = memoffset[1]
        finsary[5] = 0x00
        finsary[6:8] = struct.pack('>H', size) 
        finsary[8:] = struct.pack(">H", writedata)

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Multiple memory area read
    def multiRead(self, memadr):
        wd = memadr.replace(' ', '').split(',')
        wdary = []
        if len(wd) > 0:
            for d in wd:
                memtype, memoffset = self.offset(d, 0)
                wdary.append(memtype)
                wdary.append(memoffset[0])
                wdary.append(memoffset[1])
                wdary.append(0x00)

        s = socket(AF_INET, SOCK_DGRAM)
        #s.settimeout(2)

        finsFrame = self.finsheader()
        finsary = bytearray(2 + len(wdary))

        finsary[0] = 0x01
        finsary[1] = 0x04
        finsary[2:] = wdary

        #finsFrame.extend(finsary)

        #s.sendto(finsFrame, self.addr)
        #rcv = s.recv(BUFSIZE)

        #s.close()

        rcv = self.SendCommand(finsary)
        readdata = rcv[14:]


        data = bytearray(len(wd) * 2)
        for pos in range(len(wd)):
            wpos = pos * 3
            wdata = readdata[wpos: wpos + 3]
            data[pos * 2] = wdata[1]
            data[pos * 2 + 1] = wdata[2]

        return data

    # Run
    def run(self, mode):
        finsary = bytearray(5)
        finsary[0] = 0x04
        finsary[1] = 0x01
        finsary[2] = 0xFF
        finsary[3] = 0xFF
        finsary[4] = mode

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Stop
    def stop(self):
        finsary = bytearray(4)
        finsary[0] = 0x04
        finsary[1] = 0x02
        finsary[2] = 0xFF
        finsary[3] = 0xFF

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Read cpu unit data
    def ReadUnitData(self):
        finsary = bytearray(3)
        finsary[0] = 0x05
        finsary[1] = 0x01
        finsary[2] = 0x00

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Read cpu unit status
    def ReadUnitStatus(self):
        finsary = bytearray(2)
        finsary[0] = 0x06
        finsary[1] = 0x01

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Read cycle time
    def ReadCycletime(self):
        finsary = bytearray(3)
        finsary[0] = 0x06
        finsary[1] = 0x20
        finsary[2] = 0x01

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Clock
    def Clock(self):
        finsary = bytearray(2)
        finsary[0] = 0x07
        finsary[1] = 0x01

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        if finsres[2] == 0x00 and finsres[3] == 0x00:
            dtAry = finsres[4:10]
            dtStr = dtAry.hex()
            PlcDateTime = datetime.strptime(dtStr, '%y%m%d%H%M%S')
        else:
            PlcDateTime = None

        return PlcDateTime

    # Set clock
    def SetClock(self, dt):
        dtStr = dt.strftime('%y%m%d%H%M%S')
        dtAry = bytes.fromhex(dtStr)

        finsary = bytearray(14)
        finsary[0] = 0x07
        finsary[1] = 0x02
        finsary[2:] = dtAry

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Error Clear
    def ErrorClear(self):
        finsary = bytearray(4)
        finsary[0] = 0x21
        finsary[1] = 0x01
        finsary[2] = 0xFF
        finsary[3] = 0xFF

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Error log read last10
    def ErrorLogRead(self):
        finsary = bytearray(6)
        finsary[0] = 0x21
        finsary[1] = 0x02
        finsary[2] = 0x00
        finsary[3] = 0x00
        finsary[4] = 0x00
        finsary[5] = 0x0A

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

    # Error log clear
    def ErrorLogClear(self):
        finsary = bytearray(2)
        finsary[0] = 0x21
        finsary[1] = 0x03

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres


    # Send fins command 
    def SendCommand(self, FinsCommand):
        s = socket(AF_INET, SOCK_DGRAM)
        #s.settimeout(2)

        finsFrame = self.finsheader() + FinsCommand

        s.sendto(finsFrame, self.addr)
        readdata = s.recv(BUFSIZE)

        s.close()

        if not(readdata[12] == 0 and readdata[13] == 0):
            raise(FinsResponseError(readdata[12:14]))

        return readdata


    def toBin(self, data):
        outdata = format(int.from_bytes(data, 'big'), 'b')

        return outdata

    def WordToBin(self, data):
        size = len(data) * 8
        strBin = format(int.from_bytes(data, 'big'), 'b')
        outdata = (('0' * (size)) + strBin) [-size:]

        return outdata

    def toInt16(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 2):
            tmpdata = arydata[idx:idx+2]
            outdata += (struct.unpack('>h',tmpdata))
        
        return outdata

    def toUInt16(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 2):
            tmpdata = arydata[idx:idx+2]
            outdata += (struct.unpack('>H',tmpdata))
        
        return outdata

    def toInt32_old(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            outdata += (struct.unpack('>i',tmpdata))
        
        return outdata

    def toInt32(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            tmpdata[0:2], tmpdata[2:4] = tmpdata[2:4], tmpdata[0:2]
            outdata += (struct.unpack('>i',tmpdata))

        return outdata

    def toUInt32(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            tmpdata[0:2], tmpdata[2:4] = tmpdata[2:4], tmpdata[0:2]
            outdata += (struct.unpack('>I',tmpdata))
        
        return outdata

    def toInt64(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            tmpdata[0:2],tmpdata[2:4],tmpdata[4:6],tmpdata[6:8] = tmpdata[6:8],tmpdata[4:6],tmpdata[2:4],tmpdata[0:2]
            outdata += (struct.unpack('>q',tmpdata))

        return outdata
        
    def toUInt64(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            tmpdata[0:2],tmpdata[2:4],tmpdata[4:6],tmpdata[6:8] = tmpdata[6:8],tmpdata[4:6],tmpdata[2:4],tmpdata[0:2]
            outdata += (struct.unpack('>Q',tmpdata))
        
        return outdata

    def toFloat(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            tmpdata[0:2], tmpdata[2:4] = tmpdata[2:4], tmpdata[0:2]
            outdata += (struct.unpack('>f', tmpdata))

        return outdata

    def toDouble(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            tmpdata[0:2],tmpdata[2:4],tmpdata[4:6],tmpdata[6:8] = tmpdata[6:8],tmpdata[4:6],tmpdata[2:4],tmpdata[0:2]
            outdata += (struct.unpack('>d', tmpdata))

        return outdata

    def toString(self, data):
        outdata = data.decode("utf-8")
        return outdata






