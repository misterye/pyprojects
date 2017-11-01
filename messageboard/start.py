#!/usr/bin/python

import os

sudoPasswd = 'Y*l*q*2252266'
command = '/home/yebin/pyprojects/messageboard/.venv/bin/python /home/yebin/pyprojects/messageboard/messageboard.py > /dev/null 2>&1 &'
os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
