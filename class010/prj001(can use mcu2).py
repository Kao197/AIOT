#########################匯入模組#########################
from umqtt.simple import MQTTClient
import machine
from time import sleep
import class010.mcu2 as mcu2
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
wi = mcu2.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP = {wi.ip}")
mqtt_client = mcu2.MQTT(
    "Kao", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60, None
)
mqtt_client.connect(None)
mqtt_client.subscribe(None, "hi", on_message)
gpio = mcu2.gpio()
light_sensor = ADC(0)
LED = mcu2.LED(gpio.D5, gpio.D6, gpio.D7, pwm=False)
LED.LED_open(0, 0, 0)

#########################主程式#########################
light_sensor_reading = 0

while True:
    mqtt_client.check_msg(None)  # 檢查是否有收到訊息，有的話就執行回調函式
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
