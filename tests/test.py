from datetime import datetime
from finscommand import fins

if __name__ == "__main__":
    # Sample
    try:
        # インスタンス作成
        # NXではポート2を使用
        finsudp = fins('192.168.251.1', 2.0)   #接続先IPアドレス, 接続先FINSアドレス, 自分FINSアドレス

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

        # D1000から1000CH分に連番を書込み
        l = list(range(1000))
        writedata = list()
        for num in range(1000):
            writedata.extend(list(int(l[num]).to_bytes(2,'big')))
        rcv = finsudp.write('D1000', writedata)
        print(rcv)

        # D110から10CH分に55を書込み
        rcv = finsudp.fill('E0_100', 10, 55)
        print(rcv)

        # 複合読出し D1000,D1010,D1020
        data = finsudp.multiRead('D1000, D1010, D1020')
        print(finsudp.toUInt16(data))

        # CPUユニット情報の読出し
        rcv = finsudp.ReadUnitData()
        print(rcv)

        # CPUユニットステータスの読出し
        rcv = finsudp.ReadUnitStatus()
        print(rcv)

        # 時間情報の読出し
        rcv = finsudp.Clock()
        print(rcv)

        # 時間情報の書込み（PCの時間を書込み）
        rcv = finsudp.SetClock(datetime.now())
        print(rcv)

        # 以下CJのみ
        isCJ = False
        if isCJ:
            # モニタモードに切り替え (0x02=Monitor 0x04=Run) (NJ/NXは非対応)
            rcv = finsudp.run(0x04)
            print(rcv)

            # プログラムモードに切り替え (NJ/NXは非対応)
            rcv = finsudp.stop()
            print(rcv)

            # サイクルタイム読出し (NJ/NXは非対応)
            rcv = finsudp.ReadCycletime()
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

#    except FinsError as e:
#        print(e)

    except Exception as e:
        print(e)
