#########################匯入模組#########################
from machine import Pin, PWM,  ADC
from time import sleep
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
light_sensor = ADC(0)
RED = Pin(gpio.D5, Pin.OUT)
GREEN = Pin(gpio.D6, Pin.OUT)  
BLUE = Pin(gpio.D7, Pin.OUT)
RED.value(0)
GREEN.value(0)
BLUE.value(0)
#########################主程式#########################
while True:
    light_sensor_reading = light_sensor.read()
    print(f"value={light_sensor_reading}, {round(light_sensor_reading/1024*100)}%")
    if light_sensor_reading > 700:  # 光線很暗
        GREEN.value(1)
        RED.value(1)
        BLUE.value(1)
    else:
        GREEN.value(0)
        RED.value(0)
        BLUE.value(0)
    sleep(1)