import machine
import time

# Set up the ADC pins (Phototransistor) and output pins (Coils)
ADC_PINS = [machine.ADC(machine.Pin(36)), machine.ADC(machine.Pin(39)), machine.ADC(machine.Pin(34)), machine.ADC(machine.Pin(35))]
OUT_PINS = [machine.Pin(23, machine.Pin.OUT), machine.Pin(22, machine.Pin.OUT), machine.Pin(16, machine.Pin.OUT), machine.Pin(17, machine.Pin.OUT)]

# Define constants
# Define the threshold values for the ADCs
ADC_THRESHOLDS = [4000, 4000, 4000, 4000]
# Define the number of consecutive samples below the threshold needed to trigger the output pulse
CONSECUTIVE_SAMPLES = 5
# Define the duration of the output pulse in milliseconds
PULSE_DURATION = 1 # ms
# Define the minimum interval between pulses in milliseconds
MIN_PULSE_INTERVAL = 5 # ms

# Initialize variables
# Number of consecutive samples below the threshold for each input
consecutive_below_thresholds = [0] * len(ADC_PINS)
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

        # Check if the ADC value is below the threshold
        if adc_value < ADC_THRESHOLDS[i]:
            consecutive_below_thresholds[i] += 1
        else:
            consecutive_below_thresholds[i] = 0

        # Check if we have enough consecutive samples below the threshold to trigger the output pulse
        if consecutive_below_thresholds[i] >= CONSECUTIVE_SAMPLES:
            # Calculate the elapsed time since the last pulse
            elapsed_time = time.ticks_diff(time.ticks_ms(), last_pulse_times[i])

            # Check if we have waited long enough to trigger another pulse
            if elapsed_time >= MIN_PULSE_INTERVAL:
            
                # Turn on the output pin
                OUT_PINS[i].value(1)
                # Set the timer to trigger after the pulse duration and call the timer_callback function
                # This will turn off the PWM signal on this coil after PULSE_DURATION ms
                TIMERS[i].init(period=PULSE_DURATION, mode=machine.Timer.ONE_SHOT, callback=lambda t: timer_callback(i=i))

                # Reset the consecutive samples counter for this input and update the last pulse time for this output
                consecutive_below_thresholds[i] = 0
                last_pulse_times[i] = time.ticks_ms()
