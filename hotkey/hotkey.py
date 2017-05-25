#!/usr/bin/python

import os
import time


import key_events



os.nice(40)

while True:
    time.sleep(.25)
    key_events.key_press('k')
