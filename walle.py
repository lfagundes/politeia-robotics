#!/usr/bin/env python

import nxt.bluesock
import time
import ipdb
from nxt.motor import Motor, PORT_A, PORT_B
from nxt.sensor import Ultrasonic, Sound, PORT_2, PORT_4

robo = nxt.bluesock.BlueSock('00:16:53:08:51:40').connect()

direita = Motor(robo, PORT_A)
esquerda = Motor(robo, PORT_B)

direita.run(-82)
esquerda.run(-80)
 
time.sleep(20)

direita.brake()
esquerda.brake()
direita.turn(-40,500)
#ipdb.set_trace()
direita.run(-82)
esquerda.run(-80)
time.sleep(7)
direita.brake()
esquerda.brake()
direita.turn(-40,500)
direita.run(-82)
esquerda.run(-80)
time.sleep(6)
direita.brake()
esquerda.brake()
