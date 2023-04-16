import machine
import time

# Set up the ADC pins (Phototransistor) and output pins (Coils)
ADC_PINS = [machine.ADC(machine.Pin(36)), machine.ADC(machine.Pin(35)), machine.ADC(machine.Pin(39)), machine.ADC(machine.Pin(34))]
OUT_PINS = [machine.Pin(23, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT), machine.Pin(17, machine.Pin.OUT), machine.Pin(16, machine.Pin.OUT)]

while True:
    for i in range(len(ADC_PINS)):
        # Read the ADC value
        adc_value = ADC_PINS[i].read()
        print("Pin", i+1, "ADC Value: " + str(adc_value))

        # Turn on coil for 5 ms
        print("Pulsing coil", i+1, end="\n\n")
        OUT_PINS[i].value(1)
        time.sleep_ms(5)
        OUT_PINS[i].value(0)

        time.sleep(5)