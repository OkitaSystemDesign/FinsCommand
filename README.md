# finscommand
OMRON PLC (FINS/UDP) communication library

## OMRONの通信プロトコルのFINSコマンドをpythonで送る
FINSコマンドはメッセージサービス用の通信コマンドでPC-PLC間やPLC-デバイス間で使用されています
ここではpythonを使ってEthernetでPLCとメッセージ通信するクラスを作りました

## 環境
python3.9  
PLC OMRON CJ/NJ/NX series  

## Install
pip install finscommand


## ファンクション一覧
|  メソッド名  |  内容  |
| --- | --- |
| read | メモリエリアの読み出し |
| write | メモリエリアへ書き込み |
| fill| メモリエリアの一括書き込み |
| run| 動作モード切り替え |
| stop| プログラムモードに切り替え |
| ReadUnitData| CPUユニット情報の読出し |
| ReadUnitStatus| CPUユニットステータスの読出し |
| ReadCycletime| サイクルタイム読出し |
| Clock| 時間情報の読出し |
| SetClock| 時間情報の書込み |
| ErrorClear| 異常解除 |
| ErrorLogRead| 異常履歴の読出し |
| ErrorLogClear| 異常履歴のクリア |
| SendCommand| その他のFINSコマンドを送信 |

## 使い方
### オブジェクトの作成 fins(IPAddress, 相手FinsAddress, 自分FinsAddress, timeout)
```python
finsudp = fins('192.168.250.1', '0.1.0', '0.10.0', 2)
```
finsクラスは通信相手のIPアドレス, 相手のFINSアドレス, 自分のFINSアドレスを指定してオブジェクトを作ります  
FINSアドレスを省略すると相手のIPアドレスの下１桁の数値をノードとして相手先FINSアドレスとします
timeoutは指定しなければデフォルト2秒です

FINSアドレスとは 「FINSネットワークアドレス . ノードアドレス . 号機アドレス」の３つの数字を . (ドット)でつなぎます
ネットワークアドレスは直接接続することを想定して 0 （自ネットワーク）にしています
ノードアドレスはIPアドレスの一番下の数値と合わせて受信側（PLC）は 1 を、送信側（PC）はIPアドレスは192.168.250.10としているので 10 としています
号機アドレスは 0 （CPU宛て）とします
### read(address, num)
```python
# E0_30000から10CH読出し
data = finsudp.read('E0_30000', 10)
```
上で作ったオブジェクトのreadメソッドでアドレスとCH数を指定して値を読み出します
アドレスはCIOは000、DMはD0、EMはE0_0、WRはW0のように指定します
読み出したデータはバイト列(bytes)で受け取ります

### write(address, data)
```python
# E0_0からdataを書込み
rcv = finsudp.write('E0_0', data)
```
writeメソッドでアドレスと書き込みデータを渡して書き込みます
書き込みデータdataはバイト列(bytes)で渡します
### fill(address, num, data)
```python
# D110から10CH分(D110-119)に55を書込み
rcv = finsudp.fill('D110', 10, 55)
```
連続したメモリエリアに同一のデータを書き込みます
### multiRead(addresses)
```python
# 複合読出し D1000,D1010,D1020
data = finsudp.multiRead('D1000, D1010, D1020')
```
メモリエリアの複合読出し
### run(mode)
```python
# 動作モード切り替え (0x02=Monitor 0x04=Run)
rcv = finsudp.run(0x02)
```
### stop()
```python
# プログラムモードに切り替え
rcv = finsudp.stop()
```
### ReadUnitData()
```python
# CPUユニット情報の読出し
rcv = finsudp.ReadUnitData()
```
レスポンス内容
|  byte数  |  4  | 20 | 20 | 40 | 12 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 内容 | 05 01 00 00  | CPUユニットの形式 | システムバージョン | システム情報 | エリア情報 |
### ReadUnitStatus()
```python
# CPUユニットステータスの読出し
rcv = finsudp.ReadUnitStatus()
```
レスポンス内容
|  byte数  |  4  | 1 | 1 | 2 | 2 | 2 | 2 | 16 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 内容 | 06 01 00 00  | 運転状態 | 動作モード | 運転停止異常情報 | 運転継続異常情報 | メッセージ有無 | 故障コード | 異常メッセージ |
### ReadCycletime()
```python
# サイクルタイム読出し
rcv = finsudp.ReadCycletime()
```
レスポンス内容
|  byte数  |  4  | 4 | 4 | 4 |
| :---: | :---: | :---: | :---: | :---: |
| 内容 | 06 20 00 00  | 平均 | 最大 | 最小 |
### Clock()
```python
# 時間情報の読出し
rcv = finsudp.Clock()
```
レスポンス type:datetime.datetime
### SetClock(datetime)
```python
# 時間情報の書込み（PCの時間を書込み）
rcv = finsudp.SetClock(datetime.now())
```
### ErrorClear()
```python
# 異常解除
rcv = finsudp.ErrorClear()
```
発生中の異常を解除
### ErrorLogRead()
```python
# 異常履歴の読出し 最新10件
rcv = finsudp.ErrorLogRead()
```
レスポンス内容
|  byte数  |  4  | 2 | 2 | 2 | 10 | ... | 10 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 内容 | 21 02 00 00  | レコード最大数 | 格納数 | 読出しレコード数 | 異常履歴データ | ... | 異常履歴データ |
### ErrorLogClear()
```python
# 異常履歴のクリア
rcv = finsudp.ErrorLogClear()
```
### SendCommand()
```python
cmd = bytearray([0x05,0x01])
rcv = finsudp.SendCommand(cmd)
```
FINSコマンドを直接送信するメソッドです

## データ変換
```python
print (finsudp.toInt16(data))
```
受け取ったデータのバイト列(bytes)を変換するためのメソッド
バイト列のデータがどのようなデータかによってメソッドが変わります

|  メソッド名  |  変換するデータの長さ  |
| --- | --- |
| toBin  | ビット列 |
| WordtoBin  | 16ビット単位のビット列 |
| toInt16  | 16bit数値 |
| toUInt16 | 16bit符号なし |
| toInt32 | 32bit数値 |
| toUInt32 | 32bit符号なし |
| toInt64 | 64bit数値 |
| toUInt64 | 64bit符号なし |
| toFloat | 浮動小数点 |
| toDouble | 倍精度 |
| toString | 文字列|


## サンプル
```python
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


```

# 説明サイト
https://osdes.com/python/plccomm/finscommand.html

# Qiita記事
https://qiita.com/OkitaSystemDesign/items/7a958388d16c162148b2
