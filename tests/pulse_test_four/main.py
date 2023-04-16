import machine
import time

# Set up the ADC pins (Phototransistor) and output pins (Coils)
ADC_PINS = [machine.ADC(machine.Pin(36)), machine.ADC(machine.Pin(35)), machine.ADC(machine.Pin(39)), machine.ADC(machine.Pin(34))]
OUT_PINS = [machine.Pin(23, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT), machine.Pin(17, machine.Pin.OUT), machine.Pin(16, machine.Pin.OUT)]


# Define constants
# Define the threshold values for the ADCs
ADC_THRESHOLDS = [4000, 4000, 4000, 4000]
# Define the duration of the output pulse in milliseconds
PULSE_DURATION = 5 # ms
# Define the minimum interval between pulses in milliseconds
MIN_PULSE_INTERVAL = 30 # ms

# Initialize variables
# Time since the last output pulse for each output
last_pulse_times = [time.ticks_ms()] * len(OUT_PINS)

# Create hardware timer for each output
TIMERS = [machine.Timer(i) for i in range(len(OUT_PINS))]

# To be called when the timer triggers
def timer_callback(i):
    print("Timer Callback", i)
    OUT_PINS[i].value(0)

while True:
    for i in range(len(ADC_PINS)):
        # Read the ADC value
        adc_value = ADC_PINS[i].read()

        #print("Index", i, "ADC Value: " + str(adc_value))
        if adc_value < ADC_THRESHOLDS[i] and time.ticks_diff(time.ticks_ms(), last_pulse_times[i]) > MIN_PULSE_INTERVAL:
            # Set the timer to trigger after the pulse duration and call the timer_callback function
            # This will turn off the current on this coil after PULSE_DURATION ms
            print("Pulsing coil", i+1)
            OUT_PINS[i].value(1)
            
            time.sleep_ms(PULSE_DURATION)
            OUT_PINS[i].value(0)
            last_pulse_times[i] = time.ticks_ms()
            #TIMERS[i].init(period=PULSE_DURATION, mode=machine.Timer.ONE_SHOT, callback=lambda t: timer_callback(i))

