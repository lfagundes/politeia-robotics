#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *

b = nxt.locator.find_one_brick()

motor = Motor(b, PORT_C)
sensor = Touch(b, PORT_1)
print "Start"
while True:
    motor.turn(100, 360)
    if sensor.get_sample():
	motor.turn(-100, 720)
