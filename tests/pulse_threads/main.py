import machine
import time

# Set up the ADC pins (Phototransistor) and output pins (Coils)
ADC_PINS = [machine.ADC(machine.Pin(36)), machine.ADC(machine.Pin(39)), machine.ADC(machine.Pin(34)), machine.ADC(machine.Pin(35))]
OUT_PINS = [machine.Pin(23, machine.Pin.OUT), machine.Pin(17, machine.Pin.OUT), machine.Pin(16, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]

# Define constants
# Define the threshold values for the ADCs
ADC_THRESHOLDS = [4000, 4000, 4000, 4000]
# Define the duration of the output pulse in milliseconds
PULSE_DURATION = 20 # ms
# Define the minimum interval between pulses in milliseconds
MIN_PULSE_INTERVAL = 30 # ms
MAX_PULSE_INTERVAL = 100 # ms
# Acceleration values
PULSE_ANTICIPATION = 10 # ms
SPEED_SCALE = 1.0 # Unitless

# Global Variables
CURRENT_PERIOD = 0 # Ticks us until sensor
CURRENT_COIL = 0

# Speed estimating thread
def pulse_pin(pin_index = None):
            OUT_PINS[pin_index].value(1)
            time.sleep_ms(PULSE_DURATION)
            OUT_PINS[pin_index].value(0)

# Initialize variables
# Time since the last output pulse for each output
last_pulse_times = [time.ticks_ms()] * len(OUT_PINS)

# Create hardware timer for each output
TIMERS = [machine.Timer(i) for i in range(len(OUT_PINS))]

# To be called when the timer triggers
def timer_callback(i):
    print("Timer Callback", i)
    OUT_PINS[i].value(0)

def poll_sensors():
    global CURRENT_PERIOD, CURRENT_COIL
    at_speed = 0
    last_pulse_time = 0
    while True:
        # Read all sensors
        adc_values = [ADC_PINS[i].read() < ADC_THRESHOLDS[i] for i in range(len(ADC_PINS))]

        # Handle if any sensors detected the ball
        for i in [i for i, e in enumerate(adc_values) if e is True]:
            CURRENT_COIL = i
            CURRENT_PERIOD = time.ticks_diff(time.ticks_ms(), last_pulse_time)
            offset = int(CURRENT_PERIOD*SPEED_SCALE - PULSE_ANTICIPATION)
            print("Current period", CURRENT_PERIOD)
            print("Predicted offset", offset)
            # If the ball is going slowly, trigger the current coil
            if  CURRENT_PERIOD > MAX_PULSE_INTERVAL:
                #t = _thread.start_new_thread(pulse_pin, (i))
                TIMERS[i].init(period=0, mode=machine.Timer.ONE_SHOT, callback=lambda t: pulse_pin(i))
                print("Pulsing coil", i+1)
                last_pulse_time = time.ticks_ms()
                at_speed=0
            # If the ball is going too fast (or lots of noise is present), do nothing
            elif CURRENT_PERIOD < MIN_PULSE_INTERVAL:
                print("Going too fast, can't keep up. Ball detected at coil", i+1)
            # If ball is fast, pre-trigger the next coil
            else:
                if at_speed == 0:
                    TIMERS[i].init(period=0, mode=machine.Timer.ONE_SHOT, callback=lambda t: pulse_pin(i))
                    at_speed=1

                nexti = (i+1) % len(ADC_PINS)
                TIMERS[nexti].init(period=offset, mode=machine.Timer.ONE_SHOT, callback=lambda t: pulse_pin(nexti))
                last_pulse_time = time.ticks_ms()+offset
                print("Preparing to pulse coil", nexti+1)

print("I am testing")
poll_sensors()
print("Done testing")
