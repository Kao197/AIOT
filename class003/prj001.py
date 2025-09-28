#########################匯入模組#########################
from machine import Pin,ADC
from time import sleep
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
light_sensor = ADC(0)
#########################主程式#########################
while True:
    light_sensor_reading = light_sensor.read()
    print(f"value={light_sensor_reading}, {round(light_sensor_reading/1024*100)}%")
    sleep(1)
        