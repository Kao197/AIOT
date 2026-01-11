#########################匯入模組#########################
from machine import Pin, I2C ,ADC
import dht
import time
import mcu
import ssd1306
import json
#########################函式與類別定義#########################
msg = ""


def on_message(topic, msg_received):
    global msg
    msg = msg_received.decode("utf-8")
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, message: {msg}")
#########################宣告與設定#########################
gpio = mcu.gpio()
wi= mcu.wifi("Singular_AI", "Singular#1234")
wi.setup(ap_active=False, sta_active=True)
if wi.connect():
    print(f"IP = {wi.ip}")
mqtt_client = mcu.MQTT(
    "Kao", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqtt_client.connect()
mqtt_client.subscribe("hi", on_message)

i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT11(Pin(gpio.D0, Pin.IN))
msg_json = {}
adc = ADC(0)
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7)
mp3 = mcu.MP3()
#########################主程式#########################
try:
    while True:
        light_value = adc.read()
        d.measure()#讀取溫濕度
        temp = d.temperature()#將溫濕度分別存在不同變數
        hum = d.humidity()
        oled.fill(0)
        oled.text(f"Humidity:{hum:02d}%", 0, 0)
        oled.text(f"Temp:{temp:02d}{'\u00b0'}C", 0, 8)
        oled.text(f"Light:{light_value}", 0, 16)
        oled.show()
        msg_json["humidity"] = hum
        msg_json["temperature"] = temp
        msg_json["light"] = light_value
        msg = json.dumps(msg_json)
        mqtt_client.publish("hi2", msg)
        mqtt_client.check_msg()
        print(f"Humidity: {hum:02d}%, Temperature: {temp:02d}{'\u00b0'}C, light:{light_value}")
        
        if "LED_ON" in msg:
            LED.LED_open(1,1,1)
        elif "LED_OFF" in msg:
            LED.LED_open(0,0,0)
        if "alert" in msg or temp >38:
            mp3.start(volume=100, song=1)
            time.sleep(16)
            mp3.stop()
            msg = ""#清空msg避免重複播放
        if msg == "break":
            break
        time.sleep(1)#DHT11讀太快會error，延遲1秒再讀取
except KeyboardInterrupt:
    pass



        