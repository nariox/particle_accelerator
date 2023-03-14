import machine
import time

# Set up the ADC pins (Phototransistor) and output pins (Coils)
ADC_PINS = [machine.Pin(36), machine.Pin(39), machine.Pin(34), machine.Pin(35)]
OUT_PINS = [machine.Pin(23, machine.Pin.OUT), machine.Pin(22, machine.Pin.OUT), machine.Pin(1, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT)]

# Define constants
# Define the threshold values for the ADCs
ADC_THRESHOLDS = [900, 900, 900, 900]
# Define the number of consecutive samples below the threshold needed to trigger the output pulse
CONSECUTIVE_SAMPLES = 5
# Define the duration of the output pulse in milliseconds
PULSE_DURATION = 10 # ms
# Configure minimum time between pulses in milliseconds
MAX_PULSE_INTERVAL = 10 # ms
# PWM frequency
PWM_FREQUENCY = 10 # Hz

# Initialize variables
# Number of consecutive samples below the threshold for each input
consecutive_below_thresholds = [0] * len(ADC_PINS)
# Time since the last output pulse for each output
last_pulse_times = [time.ticks_ms()] * len(OUT_PINS)
# Create hardware timer for each output
timers = [machine.Timer(i) for i in range(len(OUT_PINS))]
# Create an instance of the PWM object for each output
pwms = [machine.PWM(pin, freq=PWM_FREQUENCY, duty=0) for pin in OUT_PINS]


# To be called when the timer triggers
def timer_callback(timer):
    pwm_index = OUT_PINS.index(timer.arg)
    pwms[pwm_index].duty(0)


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
            # Calculate the elapsed time since the last pulse for this output
            elapsed_time = time.ticks_diff(time.ticks_ms(), last_pulse_times[i])

            # Check if we have waited long enough to trigger another pulse for this output
            if elapsed_time >= MAX_PULSE_INTERVAL:
                # Turn on the output pin PWM signal for this output
                pwms[i].duty(5)
            
                # Set the timer to trigger after the pulse duration and call the timer_callback function
                # This will turn off the PWM signal on this coil after PULSE_DURATION ms
                timers[i].init(period=PULSE_DURATION, mode=machine.Timer.ONE_SHOT, arg=OUT_PINS[i], callback=timer_callback)

                # Reset the consecutive samples counter for this input and update the last pulse time for this output
                consecutive_below_thresholds[i] = 0
                last_pulse_times[i] = time.ticks_ms()
