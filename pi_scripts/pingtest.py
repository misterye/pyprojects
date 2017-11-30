#!/usr/bin/python

import os
from time import sleep

while True:
    hostname = '10.8.0.1'
    response = os.system('ping -c 3' + hostname)
    print(response)

    if response == 512:
        print 'Connected!'
    else:
        print 'Disconnected!'
        os.system('sudo /etc/init.d/openvpn restart')
        #sudoPasswd = '840821'
        #command = '/etc/init.d/openvpn restart'
        #os.system('echo %s | sudo -S %s' % (sudoPasswd, command))

    sleep(1800)
