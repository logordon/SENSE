import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
#GPIO_TRIGECHO = 15

print "Ultrasonic Measurement"

# Set pins as output and input
#GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)  # Initial state as output
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

# Set trigger to False (Low)
#GPIO.output(GPIO_TRIGECHO, False)
GPIO.output(15,False)
GPIO.output(18,False)

def measure(GPIO_TRIGECHO):
  # This function measures a distance
  # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
  #ensure start time is set in case of very quick return
    start = time.time()

  # set line to input to check for start of echo response
    GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
    while GPIO.input(GPIO_TRIGECHO)==0:
        start = time.time()

  # Wait for end of echo response
    while GPIO.input(GPIO_TRIGECHO)==1:
        stop = time.time()
  
    GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    GPIO.output(GPIO_TRIGECHO, False)

    elapsed = stop-start
    distance = (elapsed * 34300)/2.0
    time.sleep(0.1)
    return distance

try:
    while True:
        distance1 = measure(15)
        print "  Distance1 : %.1f cm" % distance1
        time.sleep(0.5)
        distance2 = measure(18)
        print "  Distance2 : %.1f cm" % distance2
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()

