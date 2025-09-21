#########################匯入模組#########################
from machine import Pin, PWM
from time import sleep
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
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
    for duty in range(1023, -1, -1):#0最亮 1023最暗
        RED.duty(duty)
        GREEN.duty(1023-duty)
        BLUE.duty(0)
        sleep(delay)
    for duty in range(1023, -1, -1):
        GREEN.duty(duty)
        BLUE.duty(1023-duty)
        sleep(delay)
    for duty in range(1023, -1, -1):
        BLUE.duty(duty)
        RED.duty(1023-duty)
        sleep(delay)