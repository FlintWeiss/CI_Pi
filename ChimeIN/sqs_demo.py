#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sqs_demo.py: get comfortable using SQS messaging


import time
import simplejson
import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Print out each queue name, which is part of its ARN
print('Queue URLs:')
for queue in sqs.queues.all():
   print(queue.url)

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='ChimeIn.fifo')

# You can now access identifiers and attributes
print 'Queue URL: ', queue.url
print 'Queue DelaySeconds: ', queue.attributes.get('DelaySeconds')


# Process messages by printing out body 
for message in queue.receive_messages():
    
   # Print out the body
   print 'Message Body: ', message.body

   # delete message (keeping commented out for now to ease testing)
   # message.delete()

