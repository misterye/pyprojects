#!/usr/bin/python

import os
from time import sleep

while True:
    #sudoPasswd = '8????1'
    #command = 'python /home/pi/Scripts/read_temp.py'
    #os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
    os.system('sudo python /home/pi/Scripts/read_temp.py')
    sleep(60)
    #break
