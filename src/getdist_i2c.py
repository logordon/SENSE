import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import subprocess
from subprocess import call

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGECHO = 14

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)  # Initial state as output

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGECHO, False)

#Create an ADS1115 instance
adc = Adafruit_ADS1x15.ADS1115()
GAIN=2

def measure():
  # This function measures a distance
  # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
    distance = [0]*3
    for i in range(3):
        distance[i] = adc.read_adc(i,gain=GAIN)

        # Distance in Inch (2^16 = 65535 for resolution)
        distance[i] = (distance[i] * 512)/65535

        # Distance in CM - 10 tolerance
        distance[i] = (distance[i] * 2.54)
        #print ("distance{0} = {1}".format(i,distance[i]))
    
    right = distance[0]
    center = distance[1]
    left = distance[2]
    
    if right < 100 and left < 100 and center <100:
        subprocess.call("aplay ~/straightahead_audio.wav", shell=True)
    elif left < 100  and right > 100 and center > 100:
        subprocess.call("aplay ~/left_audio.wav", shell=True)
    elif right < 100 and left > 100 and center > 100:
        subprocess.call("aplay ~/right_audio.wav", shell=True)
    elif left < 100 and center < 100 and right > 100:
        subprocess.call("aplay ~/centerleft_audio.wav", shell=True)
    elif right < 100 and center < 100 and left > 100:
        subprocess.call("aplay ~/centerright_audio.wav", shell=True)

try:
    while True:
        measure()
        time.sleep(2)

except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()

