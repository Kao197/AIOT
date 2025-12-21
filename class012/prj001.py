#########################匯入模組#########################
from umqtt.simple import MQTTClient
import machine
from time import sleep
import mcu
import sys
from machine import Pin, ADC, I2C
import ssd1306  # 不用管黃色底線

#########################函式與類別定義#########################
msg = ""


def on_message(topic, msg_received):
    global msg
    msg = msg_received.decode("utf-8")
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, message: {msg}")


def wrap_text(text, max_width=64):
    """
    根據螢幕寬度自動換行
    假設每個字符寬度約8像素（預設字體）
    """
    chars_per_line = max_width // 8
    lines = []
    for i in range(0, len(text), chars_per_line):
        lines.append(text[i : i + chars_per_line])
    return lines


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP = {wi.ip}")
mqtt_client = mcu.MQTT(
    "Kao", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqtt_client.connect()
mqtt_client.subscribe("hi", on_message)
gpio = mcu.gpio()
i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#########################主程式#########################
light_sensor_reading = 0
last_msg = ""

while True:
    mqtt_client.check_msg()
    sleep(0.1)  # 延遲0.1秒

    # 只在訊息改變時才更新螢幕
    if msg != last_msg:
        last_msg = msg
        oled.fill(0)  # 清除螢幕

        # 文字換行顯示
        lines = wrap_text(msg, max_width=128)
        for index, line in enumerate(lines):
            y_position = index * 8  # 每行間距8像素
            if y_position < 64:  # 確保不超出螢幕高度
                oled.text(line, 0, y_position)

        oled.show()  # 更新顯示內容
