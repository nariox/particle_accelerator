from rotary import Encoder
from machine import Pin

# Set up rotary encoder pins
pin_clk = Pin(14, Pin.IN)
pin_dt = Pin(12, Pin.IN)
pin_sw = Pin(13, Pin.IN)

# Initialize rotary encoder
encoder = Encoder(pin_clk, pin_dt, pin_sw)

# Loop to continuously read and print encoder position
while True:
    position = encoder.position
    print("Encoder position:", position)
