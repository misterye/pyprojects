#!/usr/bin/python

import os

sudoPasswd = 'Y*l*q*2252266'
command = '/home/yebin/pyprojects/mainpage/.venv/bin/python /home/yebin/pyprojects/mainpage/app.py > /dev/null 2>&1 &'
os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
