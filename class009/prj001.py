#########################匯入模組#########################
from umqtt.simple import MQTTClient
import machine
from time import sleep
import mcu
import sys
from machine import Pin, PWM, ADC


#########################函式與類別定義#########################
msg = ""


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
light_sensor = ADC(0)
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7, pwm=False)
LED.LED_open(0, 0, 0)

#########################主程式#########################
light_sensor_reading = 0

while True:
    mqClient0.check_msg()  # 檢查是否有收到訊息，有的話就執行回調函式
    mqClient0.ping()  # 發送ping給伺服器，保持連線
    sleep(0.1)  # 延遲0.1秒
    if msg == "on":
        LED.LED_open(1, 1, 1)
    elif msg == "off":
        LED.LED_open(0, 0, 0)
    elif msg == "auto":
        light_sensor_reading = light_sensor.read()
        print(f"value={light_sensor_reading}, {round(light_sensor_reading/1024*100)}%")
        if light_sensor_reading > 700:  # 光線很暗
            LED.LED_open(1, 1, 1)
        else:
            LED.LED_open(0, 0, 0)
    sleep(1)
