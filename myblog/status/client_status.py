import os
from influxdb import InfluxDBClient
from time import sleep
import MySQLdb

influxclient = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')

db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog", charset="utf8")
cur = db.cursor()
cur.execute("""SELECT client, ip FROM terminals""")
allclients = cur.fetchall()
while True:
    for c in allclients:
        ping_command = 'ping -w 1 -c 1 -i 0.2 -q ' + c[1]
        response = os.system(ping_command)
        if response == 0:
            json_body = [
                {
                    "measurement": "status",
                    "fields": {
                        "client": c[0],
                        "status": "on"
                    }
                }
            ]
            influxclient.write_points(json_body)
        else:
            json_body = [
                {
                    "measurement": "status",
                    "fields": {
                        "client": c[0],
                        "status": "off"
                    }
                }
            ]
            influxclient.write_points(json_body)
    sleep(30)
