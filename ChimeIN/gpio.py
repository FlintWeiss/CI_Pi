#!/usr/bin/env python
#


import RPi.GPIO as GPIO
import time
import simplejson


#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Light up button:
# GPIO 5 is power
# GPIO 21 will read ground/LOW when button pressed
GPIO.setup(5,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def puttonPush(channel):
    print 'PUSHED!'

# create a singe callback for the falling even (GND) and ignore more for 200ms
GPIO.add_event_detect(21, GPIO.FALLING, puttonPush, bouncetime=200)

#GPIO.add_event_callback(21, puttonPush)



# turn on the light in the button
GPIO.output(5, GPIO.HIGH)

time.sleep(2)

# turn off the light
GPIO.output(5, GPIO.LOW)

time.sleep(15)


GPIO.cleanup()

