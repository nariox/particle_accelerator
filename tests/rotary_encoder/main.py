from rotary_irq_esp import RotaryIRQ
from machine import Pin
import time

print("starting")

# Set up rotary encoder pins
#pin_clk = Pin(14, Pin.IN) # CLK
#pin_dt = Pin(12, Pin.IN)  # DT

pin_clk = 27
pin_dt = 14

# Six Wire Cable
# 1 - GND
# 2 - (+5V)

# Initialize rotary encoder object
"""
encoder = RotaryIRQ(pin_num_clk=pin_clk, 
              pin_num_dt=pin_dt, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
"""
# Set up button pin
pin_btn = Pin(12, Pin.IN, Pin.PULL_DOWN)



# Define button callback function
def button_callback(pin):
    print("Button pressed!")

# Set up interrupt handler for button press
pin_btn.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)

# Loop to continuously read and print encoder position
#while True:
#    position = encoder.value()
#    print("Encoder position:", position)
