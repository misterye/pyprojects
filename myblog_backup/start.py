#!/usr/bin/python

import os

sudoPasswd = 'Y*l*q*2252266'
command = '/home/yebin/pyprojects/myblog/.venv/bin/python /home/yebin/pyprojects/myblog/app.py > /dev/null 2>&1 &'
os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
