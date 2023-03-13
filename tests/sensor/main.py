from machine import ADC, Pin

# Define the ADC object and the GPIO pin
adc = ADC(Pin(36))

# Read and print the ADC value continuously
while True:
    value = adc.read()
    print("ADC value:", value)
