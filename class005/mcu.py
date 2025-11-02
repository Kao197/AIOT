import network


class gpio:
    def __init__(self):
        self._D0 = 16
        self._D1 = 5
        self._D2 = 4
        self._D3 = 0
        self._D4 = 2
        self._D5 = 14
        self._D6 = 12
        self._D7 = 13
        self._D8 = 15
        self._SDD3 = 10
        self._SDD2 = 9

    @property
    def D0(self):
        return self._D0

    @property
    def D1(self):
        return self._D1

    @property
    def D2(self):
        return self._D2

    @property
    def D3(self):
        return self._D3

    @property
    def D4(self):
        return self._D4

    @property
    def D5(self):
        return self._D5

    @property
    def D6(self):
        return self._D6

    @property
    def D7(self):
        return self._D7

    @property
    def D8(self):
        return self._D8

    @property
    def SDD3(self):
        return self._SDD3

    @property
    def SDD2(self):
        return self._SDD2


class wifi:
    def __init__(self, ssid=None, password=None):
        """
        初始化 WIFI 模組
        ssid: WIFI 名稱
        password: WIFI 密碼
        """
        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self.ssid = ssid
        self.password = password
        self.ap_active = False
        self.sta_active = False
        self.ip = None

    def setup(self, ap_active=False, sta_active=False):
        """
        設定WIFI模組
        ap_active: 是否啟用AP模式
        sta_active: 是否啟用STA模式
        使用方法:
        wi.setup(ap_active = True|False, sta_active = True|False)
        ||是or,&&是and.在語意上|是or,可是寫程式時要是||
        """
        self.ap_active = ap_active
        self.sta_active = sta_active
        self.ap.active(self.ap_active)
        self.sta.active(self.sta_active)

    def scan(self):
        """
        搜尋 WIFI
        返回: WIFI 列表

        使用方法:
        wi.scan()
        """
        if self.sta_active:
            wifi_list = self.sta.scan()
            print("Scan result:")
            for i in range(len(wifi_list)):
                print(wifi_list[i][0])
        else:
            print("STA 模式未啟用")

    def connect(self, ssid=None, password=None) -> bool:
        """
        連接 WIFI
        ssid: WIFI 名稱
        password: WIFI 密碼

        使用方法:
        wi.connect("WIFI_NAME", "PASSWORD")
        或在初始化時有設定過就可以不用再設定
        wi.connect()
        """
        ssid = ssid if ssid is not None else self.ssid
        password = password if password is not None else self.password

        if not self.sta_active:
            print("STA 模式未啟動")
            return False
        if ssid is None or password is None:
            print("SSID(WIFI名稱) 或密碼未設定")
            return False
        if self.sta_active:
            self.sta.connect(ssid, password)
            while not (self.sta.isconnected()):
                pass
            self.ip = self.sta.ifconfig()[0]  # 取得IP位址
            print("connect successfully", self.sta.ifconfig())
            return True
