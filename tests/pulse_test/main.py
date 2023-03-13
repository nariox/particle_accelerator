import machine
import time

# Set up the ADC pin (Phototransistor) and output pin (Coil)
adc = machine.ADC(machine.Pin(36))
out_pin = machine.Pin(23, machine.Pin.OUT)

# Define constants
# Define the threshold value for the ADC
ADC_THRESHOLD = 900
# Define the number of consecutive samples below the threshold needed to trigger the output pulse
CONSECUTIVE_SAMPLES = 5
# Define the maximum duty cycle for the output pulse (%)
MAX_DUTY_CYCLE = 2 # %
# Define the duration of the output pulse in seconds
PULSE_DURATION = 0.0005

# Initialize variables
# Number of consecutive samples below the threshold
consecutive_below_threshold = 0
# Convert Duty Cycle to fraction
max_duty_cycle = MAX_DUTY_CYCLE / 100
# Time since the last output pulse
last_pulse_time = time.ticks_ms()

while True:
    # Read the ADC value
    adc_value = adc.read()
    #print(adc_value)

    # Check if the ADC value is below the threshold
    if adc_value < ADC_THRESHOLD:
        consecutive_below_threshold += 1
    else:
        consecutive_below_threshold = 0

    # Check if we have enough consecutive samples below the threshold to trigger the output pulse
    if consecutive_below_threshold >= CONSECUTIVE_SAMPLES:
        # Calculate the elapsed time since the last pulse
        elapsed_time = time.ticks_diff(time.ticks_ms(), last_pulse_time)

        # Calculate the maximum time allowed between pulses based on the max duty cycle
        max_pulse_interval = (1 - max_duty_cycle) * elapsed_time
        print("Max Pulse Interval:", max_pulse_interval)

        # Check if we have waited long enough to trigger another pulse
        if elapsed_time >= max_pulse_interval:
            # Trigger the output pin to go high for the pulse duration
            out_pin.value(1)
            print("Pulsing! ADC:", adc_value, "Elapsed:", elapsed_time, "Consecutive:", consecutive_below_threshold)
            time.sleep(PULSE_DURATION)
            out_pin.value(0)
        
            # Reset the consecutive samples counter and update the last pulse time
            consecutive_below_threshold = 0
            last_pulse_time = time.ticks_ms()