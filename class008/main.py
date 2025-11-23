#########################匯入模組#########################
from umqtt.simple import MQTTClient
import machine
import time
import mcu
import sys
from machine import Pin


#########################函式與類別定義#########################
msg = 0


def on_message(topic, msg_received):
    global msg
    msg = msg_received.decode("utf-8")
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, message: {msg}")


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP = {wi.ip}")
mq_server = "mqtt.singularinnovation-ai.com"  # mq_server="192.168.68.114"
mqttClientId = "Kao"  # 大家要不一樣，只能用英文
mqtt_user_name = "singular"
mqtt_password = "Singular#1234"
mqClient0 = MQTTClient(
    mqttClientId, mq_server, user=mqtt_user_name, password=mqtt_password, keepalive=60
)

try:
    mqClient0.connect()
except:
    sys.exit()
finally:  # 不論成功或失敗都會執行
    print("connected MQTT server")

mqClient0.set_callback(on_message)  # 設定接收訊息的時候要執行的函式
mqClient0.subscribe("hi")  # 訂閱主題
gpio = mcu.gpio()
RED = Pin(gpio.D5, Pin.OUT)
GREEN = Pin(gpio.D6, Pin.OUT)
BLUE = Pin(gpio.D7, Pin.OUT)

#########################主程式#########################
while True:
    mqClient0.check_msg()  # 檢查是否有收到訊息，有的話就執行回調函式
    mqClient0.ping()  # 發送ping給伺服器，保持連線
    time.sleep(0.1)  # 延遲0.1秒
    if msg == "on":
        RED.value(1)
        GREEN.value(1)
        BLUE.value(1)
    elif msg == "off":
        RED.value(0)
        GREEN.value(0)
        BLUE.value(0)
