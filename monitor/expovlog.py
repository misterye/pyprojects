#!/usr/bin/python

import os
from time import sleep

while True:
    sudoPasswd = 'Y*l*q*2252266'
    command = "cat /etc/openvpn/openvpn-status.log > /home/yebin/pyprojects/monitor/vlog.log"
    os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
    sleep(5)
