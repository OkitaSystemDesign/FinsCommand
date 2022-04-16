#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

from datetime import datetime
from socket import *
import struct

BUFSIZE = 4096

class fins:
    addr = ()
    destfins = []
    srcfins = []
    port = 9600
    

    def __init__(self, host, destfinsadr, srcfinsadr):
        self.addr = host, self.port
        self.destfins = destfinsadr.split('.')
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
            moffset = list((int(adr[1:])+offset).to_bytes(2,'big'))
        elif mtype == 'W':
            mtype = 0xB1
            moffset = list((int(adr[1:]).offset).to_bytes(2,'big'))
        
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
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))
        s.settimeout(2)

        finsFrame = self.finsheader()
        finsary = bytearray(8)

        readnum = readsize // 990
        remainder = readsize % 990

        data = bytes()
        for cnt in range(readnum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == readnum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
                
            finsary[0] = 0x01
            finsary[1] = 0x01
            finsary[2] = memtype
            finsary[3] = memoffset[0]
            finsary[4] = memoffset[1]
            finsary[5] = 0x00
            finsary[6] = rsize[0]
            finsary[7] = rsize[1]

            finsFrame.extend(finsary)

            s.sendto(finsFrame, self.addr)
            readdata = s.recv(BUFSIZE)

            data += readdata[14:]

        return data

    # Memory area write
    def write(self, memaddr, writedata):
        if len(writedata) % 2 == 1:
            return
        writeWordSize = len(writedata) // 2
        
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))
        s.settimeout(2)

        finsFrame = self.finsheader()
        finsary = bytearray(8 + len(writedata))

        writenum = writeWordSize // 990
        remainder = writeWordSize % 990

        finsres = bytes()
        for cnt in range(writenum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == writenum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
                
            finsary[0] = 0x01
            finsary[1] = 0x02
            finsary[2] = memtype
            finsary[3] = memoffset[0]
            finsary[4] = memoffset[1]
            finsary[5] = 0x00
            finsary[6] = rsize[0]
            finsary[7] = rsize[1]
            finsary[8:] = writedata

            finsFrame.extend(finsary)

            s.sendto(finsFrame, self.addr)
            rcv = s.recv(BUFSIZE)

            if rcv[12] != 0 & rcv[13] != 0:
                break

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

        rcv = finsudp.SendCommand(finsary)
        finsres = rcv[10:]

        return finsres

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
        finsary = bytearray(3)
        finsary[0] = 0x07
        finsary[1] = 0x01

        rcv = self.SendCommand(finsary)
        finsres = rcv[10:]

        if finsres[2] == 0x00 and finsres[3] == 0x00:
            dtAry = finsres[4:10]
            dtStr = dtAry.hex()
            PlcDateTime = datetime.datetime.strptime(dtStr, '%y%m%d%H%M%S')
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
        s.bind(('', self.port))
        s.settimeout(2)

        finsFrame = self.finsheader() + FinsCommand
        #finsFrame.extend(FinsCommand)

        s.sendto(finsFrame, self.addr)
        readdata = s.recv(BUFSIZE)

        return readdata


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

    def toInt32(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            outdata += (struct.unpack('>i',tmpdata))
        
        return outdata
            
    def toUInt32(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            outdata += (struct.unpack('>I',tmpdata))
        
        return outdata

    def toInt64(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            outdata += (struct.unpack('>q',tmpdata))
        
    def toUInt64(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            outdata += (struct.unpack('>Q',tmpdata))
        
        return outdata

    def toFloat(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 4):
            tmpdata = arydata[idx:idx+4]
            a = tmpdata[::-1]
            a[0],a[1] = a[1],a[0]
            a[2],a[3] = a[3],a[2]

            outdata += (struct.unpack('>f', a))
        return outdata

    def toDouble(self, data):
        outdata = []
        arydata = bytearray(data)
        for idx in range(0, len(arydata), 8):
            tmpdata = arydata[idx:idx+8]
            a = tmpdata[::-1]
            a[0],a[1] = a[1],a[0]
            a[2],a[3] = a[3],a[2]
            a[4],a[5] = a[5],a[4]
            a[6],a[7] = a[7],a[6]

            outdata += (struct.unpack('>d', a))
        return outdata

    def toString(self, data):
        s = [0]*len(data)
        for i in range(0, len(data), 2):
            s[i] = data[i+1]
            s[i+1] = data[i]
        
        b = bytes(s).decode("utf-8").replace("\00","")

        return b

# Sample
# インスタンス作成
finsudp = fins('192.168.0.21', '0.21.0', '0.12.0')

# D100から10CH分のデータを読出し
data = finsudp.read('D100', 10)
print (finsudp.toInt16(data))

# E0_0から上で読み出したデータを10CH分を書込み
rcv = finsudp.write('E0_0', data)
print(rcv)

# D110から10CH分に55を書込み
rcv = finsudp.fill('D110', 10, 55)
print(rcv)

# モニタモードに切り替え (0x02=Monitor 0x04=Run)
rcv = finsudp.run(0x02)
print(rcv)

# プログラムモードに切り替え
rcv = finsudp.stop()
print(rcv)

# CPUユニット情報の読出し
rcv = finsudp.ReadUnitData()
print(rcv)

# CPUユニットステータスの読出し
rcv = finsudp.ReadUnitStatus()
print(rcv)

# サイクルタイム読出し
rcv = finsudp.ReadCycletime()
print(rcv)

# 時間情報の読出し
rcv = finsudp.Clock()
print(rcv)

# 時間情報の書込み（PCの時間を書込み）
rcv = finsudp.SetClock(datetime.now())
print(rcv)

# 異常解除
rcv = finsudp.ErrorClear()
print(rcv)

# 異常履歴の読出し 最新10件
rcv = finsudp.ErrorLogRead()
print(rcv)

# 異常履歴のクリア
rcv = finsudp.ErrorLogClear()
print(rcv)


# その他のFINSコマンドを送信するときはこちら
# 例）0x05 0x01 0x01 CPUユニット情報の読出し
cmd = bytearray([0x05,0x01])
rcv = finsudp.SendCommand(cmd)
print(rcv)
