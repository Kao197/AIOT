import network
import sys
from machine import PWM, Pin, UART
from umqtt.simple import MQTTClient


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


class LED:
    def __init__(self, r_pin, g_pin, b_pin, pwm: bool = False):
        """
        LED類別用於管理RGB LED

        屬性:
             RED(Pin):紅色LED。
             GREEN(Pin):綠色LED。
             BLUE(Pin):藍色LED。
        方法:
             __init__(r_pin, g_pin, b_pin, pwm=False):初始化LED。
             當 pwm=False 時，使用 Pin 控制 LED。
             當 pwm=True 時，使用 PWM 控制 LED。
             RED.value(value):設定紅色LED的狀態或亮度。
             GREEN.value(value):設定綠色LED的狀態或亮度。
             BLUE.value(value):設定藍色LED的狀態或亮度。
             RED.duty(duty):設定紅色LED的PWM佔空比(僅當 pwm=True 時可用)。
             GREEN.duty(duty):設定綠色LED的PWM佔空比(僅當 pwm=True 時可用)。
             BLUE.duty(duty):設定藍色LED的PWM佔空比( 僅當 pwm=True 時可用)。
        """
        self.pwm = pwm
        if pwm == False:
            self.RED = Pin(r_pin, Pin.OUT)
            self.GREEN = Pin(g_pin, Pin.OUT)
            self.BLUE = Pin(b_pin, Pin.OUT)
        else:
            frequency = 1000  # 設定 PWM 頻率為 1000Hz
            duty_cycle = 0
            self.RED = PWM(Pin(r_pin), freq=frequency, duty=duty_cycle)
            self.GREEN = PWM(Pin(g_pin), freq=frequency, duty=duty_cycle)
            self.BLUE = PWM(Pin(b_pin), freq=frequency, duty=duty_cycle)

    def LED_open(self, RED_value, GREEN_value, BLUE_value):
        """
        LED開啟方法
        LED_open(RED_value, GREEN_value, BLUE_value)
        例如:
        led = LED(r_pin=5, g_pin=6, b_pin=7, pwm=False)
        led.LED_open(1, 0, 0)  # 開啟RED_LED, 關閉GREEN_LED和BLUE_LED

        led = LED(r_pin=5, g_pin=6, b_pin=7, pwm=True)
        led.LED_open(512, 0, 0)  # 設定RED_LED亮度為512, 關閉GREEN_LED和BLUE_LED
        """
        if self.pwm == False:
            self.RED.value(RED_value)
            self.GREEN.value(GREEN_value)
            self.BLUE.value(BLUE_value)
        else:
            self.RED.duty(RED_value)
            self.GREEN.duty(GREEN_value)
            self.BLUE.duty(BLUE_value)


class MQTT:
    """
    MQTT類別用於管理MQTT連接
    屬性:
         client_id(str): 客戶端ID。
         server(str): MQTT伺服器地址。
         user(str): 使用者名稱。
         password(str): 使用者密碼。
         keepalive(int): 保持連線時間間隔。
    方法:
         connect(): 連接到MQTT伺服器。
         subscribe(topic, message): 訂閱主題並設置回調函式。
         check_msg(): 檢查是否有收到訊息並保持連線。
    """

    def __init__(self, client_id, server, user, password, keepalive):
        """
        初始化MQTT類別。
        client_id(str): MQTT客戶端ID。
        server(str): MQTT伺服器地址。
        user(str): 使用者名稱。
        password(str): 使用者密碼。
        keepalive(int): 保持連線時間間隔。
        """
        self.client_id = client_id
        self.server = server
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.client = MQTTClient(
            self.client_id,
            self.server,
            user=self.user,
            password=self.password,
            keepalive=self.keepalive,
        )

    def connect(self):
        """
        連接到MQTT伺服器。
        """
        try:
            self.client.connect()
        except:
            sys.exit()
        finally:  # 不論成功或失敗都會執行
            print("connected MQTT server")

    def subscribe(self, topic: str, on_message: function):
        """
        訂閱一個主題。

        參數:
        topic (str): 要訂閱的主題名稱。
        on_message (function): 收到訊息時要執行的回調函式。
        """
        self.client.set_callback(on_message)  # 設定接收訊息的時候要執行的函式
        self.client.subscribe(topic)  # 訂閱主題

    def check_msg(self):
        """
        檢查是否有收到訊息並保持連線。
        """
        self.client.check_msg()  # 檢查是否有收到訊息，有的話就執行回調函式
        self.client.ping()  # 發送ping給伺服器，保持連線

    def publish(self, topic: str, msg: str):
        topic = topic.encode("utf-8")
        msg = msg.encode("utf-8")
        self.client.publish(topic, msg)


class MP3:
    def __init__(self):
        """
        初始化 MP3 撥放器模組
        使用 UART1, 鮑率為 9600

        使用方法:
        mp3 = MP3()
        """
        self.uart = UART(1, baudrate=9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)

    def start(self, volume=100, song=1):  # volume最大值為0x7F(127)
        """
        播放指定音樂

        參數:
             volume (int): 音量大小,範圍0x00到0x7F(0~127),預設值為0x64(100)。
             song (int): 要播放的音樂編號(0~16),預設值為0x01(1)。

        使用方法:
            mp3.start(volume=0x64, song=0x01)
        """
        volume = int(hex(volume), 16)
        song = int(hex(song), 16)
        # volume control (13)
        # command : AA 13 01 VOL SM
        buf1 = bytearray(5)
        buf1[0] = 0xAA
        buf1[1] = 0x13
        buf1[2] = 0x01
        buf1[3] = volume
        buf1[4] = buf1[0] + buf1[1] + buf1[2] + buf1[3]
        self.uart.write(buf1)

        # specify song (07)
        # command : AA 07 02 filename(Hi) filename(Lw) SM
        buf = bytearray(6)
        buf[0] = 0xAA
        buf[1] = 0x07
        buf[2] = 0x02
        buf[3] = 0x00  # 音樂檔案開頭名稱的16進制
        buf[4] = song  # 音樂檔案結尾名稱的16進制
        buf[5] = buf[0] + buf[1] + buf[2] + buf[3] + buf[4]
        self.uart.write(buf)

    def stop(self):
        """
        停止播放

        使用方法:
            mp3.stop()
        """
        # stop (04)
        # command : AA 04 00 AE
        buf = bytearray(4)
        buf[0] = 0xAA
        buf[1] = 0x04
        buf[2] = 0x00
        buf[3] = 0xAE
        self.uart.write(buf)
