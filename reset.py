#!/usr/bin/env python

import time, random

import nxt.bluesock
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
        
    def walk(self):
        self.state = self.STATE_WALKING
    def walk_back(self):
        self.state = self.STATE_WALKING_BACK
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
                self.right.run(-75)
                self.left.run(-75)
                time.sleep(0.1)

            while self.state == self.STATE_WALKING_BACK:
                self.right.run(75)
                self.left.run(75)
                time.sleep(0.1)

            while self.state == self.STATE_TURNING_RIGHT:
                self.right.idle()
                self.left.idle()
                self.right.run(75)
                #self.left.run(-70)
                time.sleep(0.1)

            while self.state == self.STATE_TURNING_LEFT:
                self.right.idle()
                self.left.idle()
                #self.right.run(-70)
                self.left.run(72)
                time.sleep(0.1)


       
class Dog(object):

    STATE_WALKING = 0
    STATE_SEARCHING = 2
    STATE_RESTING = 1
    
    def __init__(self):
        self.brick = nxt.bluesock.BlueSock('00:16:53:08:51:40').connect()
        self.right = Motor(self.brick, PORT_A)
        self.left = Motor(self.brick, PORT_C)
        self.legs = Legs(self.right, self.left)
        
        #self.ear = Sound(self.brick, PORT_2)
        self.sonic = Ultrasonic(self.brick, PORT_4)

        self.owner_distance = 0

        self.stamina = 200

    @property
    def distance_ahead(self):
        return self.sonic.get_distance()

    def tire(self):
        self.stamina -= 1
        
    def rest(self):
        self.state = self.STATE_RESTING
        print "Resting"

        self.stop()
        
        time.sleep(random.randint(30, 90))

        self.stamina = 200

        return self.walk()

    def walk(self):
        self.state = self.STATE_WALKING
        print "Walking"

        self.legs.walk()

        while True:
            if self.distance_ahead < 40:
                return self.search()

            self.tire()

            if self.stamina == 0:
                return self.rest()

    def search(self):
        self.state = self.STATE_SEARCHING
        print "Searching"
        
        angle = 0.5
        max_angle = 15
        direction = random.choice((-1, 1))

        while angle < max_angle:
            start = time.time()
            while self.distance_ahead > 100 and time.time() < start + angle:
                self.legs.turn(direction)
            self.legs.stop()
            if self.distance_ahead <= 100:
                return self.walk()
            direction *= -1
            angle *= 1.5

            self.tire()

            if self.stamina == 0:
                return self.rest()

        return self.walk()

    def stop(self):
        self.legs.stop()


if __name__ == '__main__':
    dog = Dog()
    print "STOP"
    dog.stop()
