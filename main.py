import machine
import time

# PWM signal for each coil
pwm_pins = [23] #, 22, 1, 3]
# Create PWM objects for each coil pin
pwm_coils = [machine.PWM(machine.Pin(pin), 5000) for pin in pwm_pins]
for coil in pwm_coils:
    # Set frequencies to 10 Hz
    coil.freq(10)
    # Set the duty cycle to 0 for each PWM
    coil.duty(0)

# Sensor pins which corelate to the coil pins
sensor_pins = [36] #, 39, 34, 35]
# Define the IR sensor thresholds, signal goes HI to LO when marble is detected
thresholds = [512] #, 512, 512, 512]  # adjust these values for your sensors


# Turn on the PWM for a given index, for 0.1 seconds
# TODO: Make this a non-blocking function
def pulse_coil(idx):
    pwm_coils[idx].duty(30)   # set duty cycle to ~3%
    time.sleep(0.1)      # wait for 0.1 seconds
    pwm_coils[idx].duty(0)    # turn off the PWM

# Define the function to handle an analog sensor reading
def on_sensor_change(pin):
    idx = sensor_pins.index(pin)  # get index of ir sensor pin
    val = machine.ADC(pin).read() # read analog value of ir sensor
    if val < thresholds[idx]:     # check if the value is below the threshold
        pulse_coil(idx)           # activate the corresponding PWM signal

# Configure the sensor pins as analog inputs
for pin in sensor_pins:
    p = machine.ADC(machine.Pin(pin))
    p.atten(machine.ADC.ATTN_11DB)   # set the attenuation to 11 dB
    p.width(machine.ADC.WIDTH_12BIT) # set the width to 12 bits

# Configure the sensor pins to trigger interrupts on value change
for pin in sensor_pins:
    p = machine.ADC(machine.Pin(pin))
    p.irq(trigger=machine.Pin.IRQ_ANYEDGE, handler=on_sensor_change)
