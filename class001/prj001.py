from machine import Pin, PWM
from time import sleep

frequency = 1000
duty_cycle = 0  
led = PWM(Pin(2), freq=frequency, duty=duty_cycle)

while True:
    for duty in range(0, 1023,1):#0最亮 1023最暗
        led.duty(duty)
        sleep(0.001)


