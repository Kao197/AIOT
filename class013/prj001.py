#########################匯入模組#########################
from machine import Pin
import dht
import time
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
d = dht.DHT11(Pin(gpio.D0, Pin.IN))
#########################主程式#########################
while True:
    d.measure()#讀取溫濕度
    temp = d.temperature()#將溫濕度分別存在不同變數
    hum = d.humidity()
    print(f"Humidity: {hum:02d}%, Temperature: {temp:02d}{'\u00b0'}C")
    time.sleep(1)#DHT11讀太快會error，延遲1秒再讀取
    