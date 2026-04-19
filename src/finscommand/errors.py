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

