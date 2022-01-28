#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

import time
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


    def read(self, memaddr, readsize):
        #print('dest net=%r node=%r unit=%r' % (destfinsnet, destfinsnode, destfinsunit))
        #print('src net=%r node=%r unit=%r' % (srcfinsnet, srcfinsnode, srcfinsunit))

        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))
        s.settimeout(2)

        # FinscCommand
        finsary = bytearray(18)
        finsary[0] = 0x80
        finsary[1] = 0x00
        finsary[2] = 0x02
        finsary[3] = int(self.destfins[0])      # Destination NetNo
        finsary[4] = int(self.destfins[1])      # Destination NodeNo
        finsary[5] = int(self.destfins[2])      # Destination UnitNo
        finsary[6] = int(self.srcfins[0])       # Source NetNo
        finsary[7] = int(self.srcfins[1])       # Source NodeNo
        finsary[8] = int(self.srcfins[2])       # Source UnitNo
        finsary[9] = 0x00                       # SID

        finsary[10] = 0x01
        finsary[11] = 0x01

        #starttime = time.time()

        readnum = readsize // 990
        remainder = readsize % 990

        data = bytes()
        for cnt in range(readnum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == readnum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
                
            finsary[12] = memtype
            finsary[13] = memoffset[0]
            finsary[14] = memoffset[1]
            finsary[15] = 0x00
            finsary[16] = rsize[0]
            finsary[17] = rsize[1]

            s.sendto(finsary, self.addr)
            #print("send: %r\n%r\n" % (self.addr, finsary))
            readdata = s.recv(BUFSIZE)

            data += readdata[14:]

        #elapsedtime = time.time() - starttime
        #print ('receive: %r Length=%r\nelapsedtime = %sms\n' % (fromaddr, len(data), str(elapsedtime * 1000)))
        return data


    def write(self, memaddr, writedata):

        if len(writedata) % 2 == 1:
            return
        writeWordSize = len(writedata) // 2
        
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))
        s.settimeout(2)

        # FinscCommand
        finsary = bytearray(18 + len(writedata))
        finsary[0] = 0x80
        finsary[1] = 0x00
        finsary[2] = 0x02
        finsary[3] = int(self.destfins[0])      # Destination NetNo
        finsary[4] = int(self.destfins[1])      # Destination NodeNo
        finsary[5] = int(self.destfins[2])      # Destination UnitNo
        finsary[6] = int(self.srcfins[0])       # Source NetNo
        finsary[7] = int(self.srcfins[1])       # Source NodeNo
        finsary[8] = int(self.srcfins[2])       # Source UnitNo
        finsary[9] = 0x00                       # SID

        finsary[10] = 0x01
        finsary[11] = 0x02

        #starttime = time.time()   

        writenum = writeWordSize // 990
        remainder = writeWordSize % 990

        finsres = bytes()
        for cnt in range(writenum + 1):
            memtype, memoffset = self.offset(memaddr, cnt * 990)
            if cnt == writenum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
                
            finsary[12] = memtype
            finsary[13] = memoffset[0]
            finsary[14] = memoffset[1]
            finsary[15] = 0x00
            finsary[16] = rsize[0]
            finsary[17] = rsize[1]

            finsary[18:] = writedata

            s.sendto(finsary, self.addr)
            #print("send: %r\n%r\n" % (self.addr, finsary))
            rcv = s.recv(BUFSIZE)

            if rcv[12] != 0 & rcv[13] != 0:
                break

        finsres = rcv[10:]

        #elapsedtime = time.time() - starttime
        #print (elapsedtime = %sms\n' % (str(elapsedtime * 1000)))
        return finsres


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


finsudp = fins('192.168.0.21', '0.21.0', '0.12.0')
data = finsudp.read('E0_30000', 10)
print (finsudp.toInt16(data))

rcv = finsudp.write('E0_0', data)
print(rcv)