# OMRONの通信プロトコルのFINSコマンドをpythonで送る
FINSコマンドはメッセージサービス用の通信コマンドでPC-PLC間やPLC-デバイス間で使用されています
ここではpythonを使ってEtherenetでPLCとメッセージ通信するクラスを作りました

## 環境
Windows10
python3.9
PLC OMRON CJ/NJ/NX series

## ファンクション一覧
|  メソッド名  |  変換するデータの長さ  |
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
### オブジェクトの作成
```python
finsudp = fins('192.168.250.1', '0.1.0', '0.10.0')
```
finsクラスは通信相手のIPアドレスと相手と自分のFINSアドレスを指定してオブジェクトを作ります
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
レスポンス内容
|  byte数  |  4  | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 内容 | 07 01 00 00  | 年 | 月 | 日 | 時 | 分 | 秒 | 曜日 |

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
# D100から10CH分のデータを読出し
data = finsudp.read('D100', 10)
print (finsudp.toInt16(data))

出力
> [1, 2, 500, 1000, 30000, 32767, -1, 0, 0, 0]
```





# Qiita記事
https://qiita.com/OkitaSystemDesign/items/7a958388d16c162148b2
