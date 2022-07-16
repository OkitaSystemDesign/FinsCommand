from datetime import datetime
from logging import exception
from socket import *
import struct

BUFSIZE = 4096

class FinsError(Exception):
    pass

class FinsResponseError(FinsError):
    def __init__(self, EndCode):
        self.endcode = EndCode.hex()
        if self.endcode == "0101":
            self.message = self.endcode + ": Local node not in network (自ノード ネットワーク未加入)"
        elif self.endcode == "0102":
            self.message = self.endcode + ": Token timeout (トークン タイムアウト)"
        elif self.endcode == "0103":
            self.message = self.endcode + ": Retries failed (再送オーバー)"
        elif self.endcode == "0104":
            self.message = self.endcode + ": Too many send frames (送信許可フレーム数オーバー)"
        elif self.endcode == "0105":
            self.message = self.endcode + ": Node address range error (ノードアドレス設定範囲エラー)"
        elif self.endcode == "0106":
            self.message = self.endcode + ": Node address duplication (ノードアドレス二重設定エラー)"
        elif self.endcode == "0201":
            self.message = self.endcode + ": Destination node not in network (相手ノード ネットワーク未加入)"
        elif self.endcode == "0202":
            self.message = self.endcode + ": Unit missing (該当ユニットなし)"
        elif self.endcode == "0203":
            self.message = self.endcode + ": Third node missing (第三ノード ネットワーク未加入)"
        elif self.endcode == "0204":
            self.message = self.endcode + ": Destination node busy (相手ノード ビジー)"
        elif self.endcode == "0205":
            self.message = self.endcode + ": Response timeout (レスポンス タイムアウト)"
        elif self.endcode == "0301":
            self.message = self.endcode + ": Communications controller error (通信コントローラ異常)"
        elif self.endcode == "0302":
            self.message = self.endcode + ": CPU Unit error (CPUユニット異常)"
        elif self.endcode == "0303":
            self.message = self.endcode + ": Controller error (該当コントローラ異常)"
        elif self.endcode == "0304":
            self.message = self.endcode + ": Unit number error (ユニット番号設定異常)"
        elif self.endcode == "0401":
            self.message = self.endcode + ": Undefined command (未定義コマンド)"
        elif self.endcode == "0402":
            self.message = self.endcode + ": Not supported by model/version (サポート外機種/バージョン)"
        elif self.endcode == "0501":
            self.message = self.endcode + ": Destination address setting error (相手アドレス設定エラー)"
        elif self.endcode == "0502":
            self.message = self.endcode + ": No routing tables (ルーチングテーブル未登録)"
        elif self.endcode == "0503":
            self.message = self.endcode + ": Routing table error (ルーチングテーブル異常)"
        elif self.endcode == "0504":
            self.message = self.endcode + ": oo many relays (中継回数オーバー)"
        elif self.endcode == "1001":
            self.message = self.endcode + ": Command too long (コマンド長オーバー)"
        elif self.endcode == "1002":
            self.message = self.endcode + ": Command too short (コマンド長不足)"
        elif self.endcode == "1003":
            self.message = self.endcode + ": Elements/data don’t match (要素数/データ数不一致)"
        elif self.endcode == "1004":
            self.message = self.endcode + ": Command format error (コマンドフォーマットエラー)"
        elif self.endcode == "1005":
            self.message = self.endcode + ": Header error (ヘッダ異常)"
        elif self.endcode == "1101":
            self.message = self.endcode + ": Area classification missing (エリア種別なし)"
        elif self.endcode == "1102":
            self.message = self.endcode + ": Access size error (アクセスサイズエラー)"
        elif self.endcode == "1103":
            self.message = self.endcode + ": Address range error (アドレス範囲外指定エラー)"
        elif self.endcode == "1104":
            self.message = self.endcode + ": Address range exceeded (アドレス範囲オーバー)"
        elif self.endcode == "1106":
            self.message = self.endcode + ": Program missing (該当プログラム番号なし)"
        elif self.endcode == "1109":
            self.message = self.endcode + ": Relational error (相関関係エラー)"
        elif self.endcode == "110A":
            self.message = self.endcode + ": Duplicate data access (データ重複エラー)"
        elif self.endcode == "110B":
            self.message = self.endcode + ": Response too long (レスポンス長オーバー)"
        elif self.endcode == "110C":
            self.message = self.endcode + ": Parameter error (パラメータエラー)"
        elif self.endcode == "2002":
            self.message = self.endcode + ": Protected (プロテクト中)"
        elif self.endcode == "2003":
            self.message = self.endcode + ": Table missing (登録テーブルなし)"
        elif self.endcode == "2004":
            self.message = self.endcode + ": Data missing (検索データなし)"
        elif self.endcode == "2005":
            self.message = self.endcode + ": Program missing (該当プログラム番号なし)"
        elif self.endcode == "2006":
            self.message = self.endcode + ": File missing (該当ファイルなし)"
        elif self.endcode == "2007":
            self.message = self.endcode + ": Data mismatch (照合異常)"
        elif self.endcode == "2101":
            self.message = self.endcode + ": Read-only (リードオンリー)"
        elif self.endcode == "2102":
            self.message = self.endcode + ": Protected (プロテクト中)"
        elif self.endcode == "2103":
            self.message = self.endcode + ": Cannot register (登録不可)"
        elif self.endcode == "2105":
            self.message = self.endcode + ": Program missing (該当プログラム番号なし)"
        elif self.endcode == "2106":
            self.message = self.endcode + ": File missing (該当ファイルなし)"
        elif self.endcode == "2107":
            self.message = self.endcode + ": File name already exists (同一ファイル名あり)"
        elif self.endcode == "2108":
            self.message = self.endcode + ": Cannot change (変更不可)"
        elif self.endcode == "2201":
            self.message = self.endcode + ": Not possible during execution (運転中のため動作不可)"
        elif self.endcode == "2202":
            self.message = self.endcode + ": Not possible while running (停止中)"
        elif self.endcode == "2203":
            self.message = self.endcode + ": Wrong PLC mode, PROGRAM mode (本体モードが違う プログラムモード)"
        elif self.endcode == "2204":
            self.message = self.endcode + ": Wrong PLC mode, DEBUG mode (本体モードが違う デバッグモード)"
        elif self.endcode == "2205":
            self.message = self.endcode + ": Wrong PLC mode, MONITOR mode (本体モードが違う モニタモード)"
        elif self.endcode == "2206":
            self.message = self.endcode + ": Wrong PLC mode, RUN mode (本体モードが違う 運転モード)"
        elif self.endcode == "2207":
            self.message = self.endcode + ": Specified node not polling node (指定ノードが管理局でない)"
        elif self.endcode == "2208":
            self.message = self.endcode + ": Step cannot be executed (ステップが実行不可)"
        elif self.endcode == "2301":
            self.message = self.endcode + ": File device missing (ファイル装置なし)"
        elif self.endcode == "2302":
            self.message = self.endcode + ": Memory missing (該当メモリなし)"
        elif self.endcode == "2303":
            self.message = self.endcode + ": Clock missing (時計なし)"
        elif self.endcode == "2401":
            self.message = self.endcode + ": Table missing (登録テーブルなし)"

        else:
            self.message = self.endcode

        self.message = "FINS ERROR " + self.message

    def __str__(self):
        return repr(self.message)


class fins:
    addr = ()
    destfins = []
    srcfins = []
    port = 9600
    

    def __init__(self, host, destfinsadr="0.0.0", srcfinsadr="0.1.0"):
        self.addr = host, self.port
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
        s = socket(AF_INET, SOCK_DGRAM)
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
        
        s.close()

        if not(readdata[12] == 0 and readdata[13] == 0):
            raise(FinsResponseError(readdata[12:14]))

        return data
            
    # Memory area write
    def write(self, memaddr, writedata):
        if len(writedata) % 2 == 1:
            return
        writeWordSize = len(writedata) // 2
        
        s = socket(AF_INET, SOCK_DGRAM)
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

        s.close()

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
        s.settimeout(2)

        finsFrame = self.finsheader()
        finsary = bytearray(2 + len(wdary))

        finsary[0] = 0x01
        finsary[1] = 0x04
        finsary[2:] = wdary

        finsFrame.extend(finsary)

        s.sendto(finsFrame, self.addr)
        readdata = s.recv(BUFSIZE)

        s.close()

        data = bytearray(len(wd) * 2)
        for pos in range(len(wd)):
            wpos = 14 + pos * 3
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
        s.settimeout(2)

        finsFrame = self.finsheader() + FinsCommand

        s.sendto(finsFrame, self.addr)
        readdata = s.recv(BUFSIZE)

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


if __name__ == "__main__":
    # Sample
    try:
        # インスタンス作成
        finsudp = fins('192.168.0.16')

        # 0CHから1CH分読出し  ビット表記
        data = finsudp.read('0', 1)
        print(finsudp.toBin(data))                  # ゼロサプレス表記
        print(finsudp.WordToBin(data))              # ゼロ埋め表記
        print(list(finsudp.WordToBin(data)))        # ゼロ埋めのリスト

        # W0から2CH分読出し  ビット表記
        data = finsudp.read('W0', 2)
        print(finsudp.toBin(data))
        print(finsudp.WordToBin(data))
        print(list(finsudp.WordToBin(data)))

        # H0から4CH分読出し  ビット表記
        data = finsudp.read('H0', 4)
        print(finsudp.toBin(data))
        print(finsudp.WordToBin(data))
        print(list(finsudp.WordToBin(data)))

        # D1000を読出し ビット表記
        data = finsudp.read('D1000', 1)
        print(finsudp.toBin(data))
        print(finsudp.WordToBin(data))
        print(list(finsudp.WordToBin(data)))

        # D1001を読出しINT
        data = finsudp.read('D1001', 1)
        print(finsudp.toInt16(data))

        # D1002-D1003を読出しDINT
        data = finsudp.read('D1002', 2)
        print(finsudp.toInt32(data))

        # D1004-D1007を読出しLINT
        data = finsudp.read('D1004', 4)
        print(finsudp.toInt64(data))

        # D1008を読出しUINT
        data = finsudp.read('D1008', 1)
        print(finsudp.toUInt16(data))

        # D1009-D1010を読出しUDINT
        data = finsudp.read('D1009', 2)
        print(finsudp.toUInt32(data))

        # D1011-D1014を読出しULINT
        data = finsudp.read('D1011', 4)
        print(finsudp.toUInt64(data))

        # D1015-D1016を読出しFLOAT
        data = finsudp.read('D1015', 2)
        print(finsudp.toFloat(data))

        # D1017-D1020を読出しDOUBLE
        data = finsudp.read('D1017', 4)
        print(finsudp.toDouble(data))

        # D1021-D1025を読出しDOUBLE
        data = finsudp.read('D1021', 5)
        print(finsudp.toString(data))


        # D1100から10CH分のデータを読出し
        data = finsudp.read('D1100', 10)
        print(finsudp.toUInt16(data))

        # E0_0から上で読み出したデータを10CH分を書込み
        rcv = finsudp.write('E0_0', data)
        print(rcv)

        # D110から10CH分に55を書込み
        rcv = finsudp.fill('E0_100', 10, 55)
        print(rcv)

        # 複合読出し D1000,D1010,D1020
        data = finsudp.multiRead('D1000, D1010, D1020')
        print(finsudp.toUInt16(data))

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

    except FinsError as e:
        print(e)

    except Exception as e:
        print(e)





