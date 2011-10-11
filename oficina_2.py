#!/usr/bin/env python

import nxt.bluesock
import time
from nxt.motor import Motor, PORT_A, PORT_B
from nxt.sensor import Ultrasonic, Sound, PORT_2, PORT_4

robo = nxt.bluesock.BlueSock('00:16:53:08:51:40').connect()

direita = Motor(robo, PORT_A)
esquerda = Motor(robo, PORT_B)

def anda(tempo):
    direita.run(-80)
    esquerda.run(-80)
	
    time.sleep(tempo)

    direita.brake()
    esquerda.brake()

# direita.turn(-70,910) 
def vira(giro):
    direita.turn(-70,giro*4.2)


anda(4)
vira(90)
anda(4)
vira(90)
anda(4)
vida(90)
anda(4)


