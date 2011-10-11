#!/usr/bin/env python

import time, random

import nxt.bluesock
import nxt.locator
import thread
from nxt.motor import Motor, PORT_A, PORT_C
from nxt.sensor import Ultrasonic, Sound, PORT_2, PORT_4

class Legs(object):

    STATE_IDLE = 0
    STATE_WALKING = 1
    STATE_WALKING_BACK = 2
    STATE_TURNING_LEFT = 3
    STATE_TURNING_RIGHT = 4

    def __init__(self, right, left):
        self.right = right
        self.left = left

        self.state = self.STATE_IDLE

        self.start()

    def _set_state_for_delay(self, state, delay):
        next_state = self.state
        def schedule():
            time.sleep(delay)
            self.state = next_state
        self.state = state
        thread.start_new_thread(schedule, tuple())
        
    def walk(self, speed = 65):
        self.state = self.STATE_WALKING
        self.speed = speed
        print "  forward speed %d" % speed
    def walk_back(self, speed = 65):
        self.state = self.STATE_WALKING_BACK
        self.speed = speed
        print "  back speed %d" % speed
    def turn(self, direction):
        if direction > 0:
            self.state = self.STATE_TURNING_LEFT
        else:
            self.state = self.STATE_TURNING_RIGHT
            
    def limited_turn(self, direction, delay = 1.5):
        if direction > 0:
            self._set_state_for_delay(self.STATE_TURNING_LEFT, delay)
        else:
            self._set_state_for_delay(self.STATE_TURNING_RIGHT, delay)
            
    def stop(self):
        self.state = self.STATE_IDLE

    def start(self):
        def run():
            self.run()
        thread.start_new_thread(self.run, tuple())

    def run(self):
        while True:
            while self.state == self.STATE_IDLE:
#                print "Idle"
                self.right.idle()
                self.left.idle()
                time.sleep(0.1)

            while self.state == self.STATE_WALKING:
                #print "Walking"
                self.right.run(-self.speed)
                self.left.run(-self.speed)
                time.sleep(0.1)

            while self.state == self.STATE_WALKING_BACK:
                self.right.run(self.speed)
                self.left.run(self.speed)
                time.sleep(0.1)

            while self.state == self.STATE_TURNING_RIGHT:
                self.right.idle()
                self.left.idle()
                self.right.run(65)
                self.left.run(-60)
                time.sleep(0.1)

            while self.state == self.STATE_TURNING_LEFT:
                self.right.idle()
                self.left.idle()
                self.right.run(-60)
                self.left.run(65)
                time.sleep(0.1)


       
class Dog(object):

    MIN_OWNER_DISTANCE = 30
    MAX_OWNER_DISTANCE = 40
    LOST_DISTANCE = 100
    
    def __init__(self):
        self.brick = nxt.bluesock.BlueSock('00:16:53:08:51:40').connect()
	#self.brick = nxt.locator.find_one_brick()
        self.right = Motor(self.brick, PORT_A)
        self.left = Motor(self.brick, PORT_C)
        self.legs = Legs(self.right, self.left)
        
        #self.ear = Sound(self.brick, PORT_2)
        self.sonic = Ultrasonic(self.brick, PORT_4)

        self.owner_distance = 0

        self.last_distance = 255

    @property
    def distance_ahead(self):
        sample = self.sonic.get_distance()
        if sample == 255:
            self.last_distance += 20
            return self.last_distance
        self.last_distance = sample
        return sample        

    def wait(self):
        print "Waiting"

        self.stop()
        
        while True:
            distance = self.distance_ahead
            if distance > 30 and distance < 40:
                self.owner_distance = distance
                print "owner distance: %d" % distance
                return self.follow()

    def follow(self):
        print "Following"

        while True:
            distance = self.distance_ahead

            if distance > self.owner_distance + 50:
                return self.search()

            if distance > self.owner_distance:
                self.legs.walk(50 + distance - self.owner_distance)
            elif distance < self.owner_distance:
                self.legs.walk_back(50 + self.owner_distance - distance)
            else:
                self.stop()
                time.sleep(0.5)

    def search(self):
        print "Searching"
        
        angle = 0.5
        max_angle = 64
        direction = random.choice((-1, 1))

        while angle < max_angle:
            start = time.time()
            while self.distance_ahead > 100 and time.time() < start + angle:
                self.legs.turn(direction)
            self.legs.stop()
            if self.distance_ahead <= 100:
                return self.follow()
            direction *= -1
            angle *= 2

        return self.wait()

    def stop(self):
        self.legs.stop()


if __name__ == '__main__':
    dog = Dog()

    dog.wait()
    sys.exit()
#    while True:
#        print dog.distance_ahead

    dog.legs.walk_back()
    cycles = 0
    while cycles < 20:
        print dog.distance_ahead
    sys.exit()

    
    try:
        dog.wait()
    finally:
        dog.stop()


    

