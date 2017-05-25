from key_events import *


import os
os.nice(40)


pos = position()

for x in range(1000):
    #time.sleep(.25)
    mouseclick(*pos)

