#!/usr/bin/python

import os

sudoPasswd = 'Y*l*q*2252266'
command = 'certbot renew'
os.system('echo %s | sudo -S %s' % (sudoPasswd, command))
