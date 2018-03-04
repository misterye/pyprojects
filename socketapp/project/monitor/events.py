# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");

#from gevent import monkey
#monkey.patch_all()
import eventlet
eventlet.monkey_patch()

from flask_socketio import emit
from openvpn_status import parse_status
from ..app import socketio, db, memoryUsage
from influxdb import InfluxDBClient
#from time import sleep

@socketio.on('my_event', namespace='/monitor')
def my_event(msg):
    emit('my_response', msg)

@socketio.on('status', namespace='/monitor')
def clientStatus():
    cur = db.connection.cursor()
    cur.execute("SELECT ip, client FROM terminals")
    allclients = cur.fetchall()
    clientlist = []
    for c in allclients:
        clientlist.append(c['client'])
    clients = {}
    for c in allclients:
        clients[c['client']] = c['ip']
    while True:
        memoryUsageStr = memoryUsage()
        influxclient = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')
        for c in clientlist:
            qstatus = "select * from status where ip=" + "\'"+clients[c]+"\'" + " order by time desc limit 1"
            statusresult = influxclient.query(qstatus)
            if statusresult:
                for sr in statusresult:
                    for s in sr:
                        conn_stat = s['connect']
                        utc_time = s['time']
                        diff = int(utc_time[11:13])+8
                        if diff >= 24:
                            local_hour = diff - 24
                        else:
                            local_hour = diff
                        replace = str(local_hour)
                        local_time = utc_time[:11] + replace + utc_time[13:]
                        conn_time = local_time[:10] + " " + local_time[11:19]
            else:
                conn_stat = 'off'
                conn_time = 'NULL'
            qtemp = "select * from temperature where client=" + "\'"+c+"\'" + " order by time desc limit 1"
            tempresult = influxclient.query(qtemp)
            if tempresult:
                for tr in tempresult:
                    for t in tr:
                        client_temp = t['tempdata']
                        utc_time = t['time']
                        diff = int(utc_time[11:13])+8
                        if diff >= 24:
                            local_hour = diff - 24
                        else:
                            local_hour = diff
                        replace = str(local_hour)
                        local_time = utc_time[:11] + replace + utc_time[13:]
                        temp_time = local_time[:10] + " " + local_time[11:19]
            else:
                client_temp = 99.9
                temp_time = 'NULL'
            emit('online', {
                'connect_time': conn_time,
                'temperature_time': temp_time,
                'memory_usage': memoryUsageStr,
                'client_name': c,
                'client_status': conn_stat,
                'client_temperature': client_temp
                })
        eventlet.sleep(10)
