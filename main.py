from machine import Pin, PWM
from time import sleep

led = PWM(Pin(23), 5000)

# freq = 10 Hz
# duty = 30
# gives about 200mA

led.freq(10)
led.duty(30)
