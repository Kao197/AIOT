#########################匯入模組#########################
from machine import Pin, I2C
import dht
import time
import mcu
import ssd1306
#########################函式與類別定義#########################

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

i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT11(Pin(gpio.D0, Pin.IN))
#########################主程式#########################
while True:
    d.measure()#讀取溫濕度
    temp = d.temperature()#將溫濕度分別存在不同變數
    hum = d.humidity()
    oled.fill(0)
    oled.text(f"Humidity:{hum:02d}%", 0, 0)
    oled.text(f"Temp:{temp:02d}{'\u00b0'}C", 0, 8)
    oled.show()
    msg = f"Humidity:{hum:02d}%, Temperature:{temp:02d}{'\u00b0'}C"
    mqtt_client.publish("hi", msg)
    print(f"Humidity: {hum:02d}%, Temperature: {temp:02d}{'\u00b0'}C")
    time.sleep(1)#DHT11讀太快會error，延遲1秒再讀取
    