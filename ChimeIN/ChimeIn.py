#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ChimeIn.py : listens to a SQS queue and everytime it sees a message, turns on the light. 
#   Has a button to clear the light.
# Intention: Used in meeting rooms where there are remote callers. The can 
#    "raise their hand to chime in to the conversation" by hitting a URL that adds SQS message to the queuue.
#    That action will turn on the light in the meeting room (on the device that this code is running on).
#    When the light comes on, the facillitator should halt the conversation in the room, ask folks on the 
#    phone for their input, and once all remote folks have had a chance to speak, press the button to 
#    reset the light so that more chime in's will be recognized.
# Concept owner and author: Flint Weiss
#


import sys
import RPi.GPIO as GPIO
import time
import simplejson
import boto3
from botocore.exceptions import ClientError
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
from max7219.led import device as led_device, matrix as led_matrix


GPIO.setmode(GPIO.BCM)

# Light up button:
# GPIO 5 is power
# GPIO 21 will read ground/LOW when button pressed
GPIO.setup(5,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
print("Created LED device")


#==========================================================================================================
# handles the buttonPush even which will reset the light
def puttonPush(channel):
    print 'PUSHED!'
    displayOff()

    # turn off the light in the button
#    GPIO.output(5, GPIO.LOW)
    buttonLightOff()

#==========================================================================================================
# turn on the light in the button
def buttonLightOn():
    GPIO.output(5, GPIO.HIGH)

#==========================================================================================================
# turn off the light in the button
def buttonLightOff():
    GPIO.output(5, GPIO.LOW)

#==========================================================================================================
# scroll message to the display
def scrollMessage(msg):
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.04)

#==========================================================================================================
def displayOn():
    print("display on")
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="white")


#==========================================================================================================
def displayOff():
    print("display off")
    #max_device.clear()
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="black", fill="black")

#----------------------------------------------------------------------------------------------------------
# main execution section

GPIO.add_event_detect(21, GPIO.FALLING, puttonPush, bouncetime=200)

scrollMessage("Hello World")

displayOn()
buttonLightOn()
time.sleep(2)
displayOff()
buttonLightOff()
time.sleep(1)

# Get the service resource
sqs = boto3.resource('sqs')
queue = None

while(True):

   if queue is None:
      # Get the queue. This returns an SQS.Queue instance
      queue = sqs.get_queue_by_name(QueueName='ChimeIn')

   try:
      for message in queue.receive_messages(MaxNumberOfMessages=10):
    
          # turn on the light in the button
          buttonLightOn()
          displayOn()

          # Print out the body
          print 'Message Body:', message.body, '<'

          # delete message (keeping commented out for now to ease testing)
          message.delete()

          if message.body == 'Flint says exit exit exit':
             print 'trying to exit'
             displayOff()
             buttonLightOff()
             scrollMessage("Exiting")
             print 'GPIO cleanup'
             GPIO.cleanup()
             print 'raising system exit exception'
             raise SystemExit

      # sleep a quarter second because we don't need to hammer SQS
      time.sleep(0.25) 

   except SystemExit:
      # have to exit from here to actually exit
      print 'sys exit'
      sys.exit()

   except:
      queue = None

# Cleanup on exit. Only for development b/c real usage will just power down the pi
GPIO.cleanup()
