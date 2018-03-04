import os
from time import sleep

try:
    while True:
        os.system('free -h > /home/yebin/pyprojects/myblog/memuse')
        f = open('memuse', 'r')
        lines = f.readlines()
        linestring = lines[1].split()
        totalstr = linestring[1]
        usedstr = linestring[2]
        freestr = linestring[3]
        sharedstr = linestring[4]
        buffstr = linestring[5]
        availablestr = linestring[6]
        memstr = "total: " + totalstr + " | " + "used: " + usedstr + " | " + "free: " + freestr + " | " + "shared: " + sharedstr + " | " + "buff/cache: " + buffstr + " | " + "available: " + availablestr
        print memstr
        sleep(10)
except KeyboardInterrupt:
    print "exiting..."