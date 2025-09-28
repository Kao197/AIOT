#########################匯入模組#########################
from machine import Pin, PWM,  ADC
from time import sleep
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
light_sensor = ADC(0)
frequency = 1000
duty_cycle = 0
RED = PWM(Pin(gpio.D5, Pin.OUT), freq=frequency, duty=duty_cycle)
GREEN = PWM(Pin(gpio.D6, Pin.OUT), freq=frequency, duty=duty_cycle)
BLUE = PWM(Pin(gpio.D7, Pin.OUT), freq=frequency, duty=duty_cycle)
delay = 0.001
RED.duty(0)
GREEN.duty(0)
BLUE.duty(0)
#########################主程式#########################
while True:
    light_sensor_reading = light_sensor.read()
    print(f"value={light_sensor_reading}, {round(light_sensor_reading/1024*100)}%")
    if light_sensor_reading<400:
        light_sensor_reading=0
    RED.duty(light_sensor_reading)
    GREEN.duty(light_sensor_reading)
    BLUE.duty(light_sensor_reading)
    sleep(0.1)