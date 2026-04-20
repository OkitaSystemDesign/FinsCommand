from datetime import datetime
from finscommand import fins

'''
# finsコマンドの送受信ログが必要な場合はコメントを外してください
import logging

logging.basicConfig(
    filename="fins.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
'''

try:
    # インスタンス作成
    # NXではポート2を使用
    f = fins("192.168.251.1")   #接続先IPアドレス (, 接続先FINSアドレス, 自分FINSアドレス, timeout)

    # 0CHから1CH分読出し  ビット表記
    data = f.read('0', 1)
    print(f.toBin(data))                  # ゼロサプレス表記
    print(f.WordToBin(data))              # ゼロ埋め表記
    print(list(f.WordToBin(data)))        # ゼロ埋めのリスト

    # W0から2CH分読出し  ビット表記
    data = f.read('W0', 2)
    print(f.toBin(data))
    print(f.WordToBin(data))
    print(list(f.WordToBin(data)))

    # H0から4CH分読出し  ビット表記
    data = f.read('H0', 4)
    print(f.toBin(data))
    print(f.WordToBin(data))
    print(list(f.WordToBin(data)))

    # D1000を読出し ビット表記
    data = f.read('D1000', 1)
    print(f.toBin(data))
    print(f.WordToBin(data))
    print(list(f.WordToBin(data)))

    # D1001を読出しINT
    data = f.read('D1001', 1)
    print(f.toInt16(data))

    # D1002-D1003を読出しDINT
    data = f.read('D1002', 2)
    print(f.toInt32(data))

    # D1004-D1007を読出しLINT
    data = f.read('D1004', 4)
    print(f.toInt64(data))

    # D1008を読出しUINT
    data = f.read('D1008', 1)
    print(f.toUInt16(data))

    # D1009-D1010を読出しUDINT
    data = f.read('D1009', 2)
    print(f.toUInt32(data))

    # D1011-D1014を読出しULINT
    data = f.read('D1011', 4)
    print(f.toUInt64(data))

    # D1015-D1016を読出しFLOAT
    data = f.read('D1015', 2)
    print(f.toFloat(data))

    # D1017-D1020を読出しDOUBLE
    data = f.read('D1017', 4)
    print(f.toDouble(data))

    # D1021-D1025を読出しDOUBLE
    data = f.read('D1021', 5)
    print(f.toString(data))


    # D1100から10CH分のデータを読出し
    data = f.read('D1100', 10)
    print(f.toUInt16(data))

    # E0_0から上で読み出したデータを10CH分を書込み
    rcv = f.write('E0_0', data)
    print(rcv)

    # D1000から1000CH分に連番を書込み
    l = list(range(1000))
    writedata = list()
    for num in range(1000):
        writedata.extend(list(int(l[num]).to_bytes(2,'big')))
    rcv = f.write('D1000', writedata)
    print(rcv)

    # D110から10CH分に55を書込み
    rcv = f.fill('E0_100', 10, 55)
    print(rcv)

    # 複合読出し D1000,D1010,D1020
    data = f.multiRead('D1000, D1010, D1020')
    print(f.toUInt16(data))

    # CPUユニット情報の読出し
    rcv = f.ReadUnitData()
    print(rcv)

    # CPUユニットステータスの読出し
    rcv = f.ReadUnitStatus()
    print(rcv)

    # 時間情報の読出し
    rcv = f.Clock()
    print(rcv)

    # 時間情報の書込み（PCの時間を書込み）
    rcv = f.SetClock(datetime.now())
    print(rcv)

    # 以下CJのみ
    isCJ = False
    if isCJ:
        # モニタモードに切り替え (0x02=Monitor 0x04=Run) (NJ/NXは非対応)
        rcv = f.run(0x04)
        print(rcv)

        # プログラムモードに切り替え (NJ/NXは非対応)
        rcv = f.stop()
        print(rcv)

        # サイクルタイム読出し (NJ/NXは非対応)
        rcv = f.ReadCycletime()
        print(rcv)

        # 異常解除
        rcv = f.ErrorClear()
        print(rcv)

        # 異常履歴の読出し 最新10件
        rcv = f.ErrorLogRead()
        print(rcv)

        # 異常履歴のクリア
        rcv = f.ErrorLogClear()
        print(rcv)


    # その他のFINSコマンドを送信するときはこちら
    # 例）0x05 0x01 0x01 CPUユニット情報の読出し
    cmd = bytearray([0x05,0x01])
    rcv = f.SendCommand(cmd)
    print(rcv)


except Exception as e:
    print(e)
