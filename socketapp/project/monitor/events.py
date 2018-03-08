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
from dateutil import parser

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
    cur.close()
    while True:
        memoryUsageStr = memoryUsage()
        influxclient = InfluxDBClient('111.47.20.166', 8086, 'admin', '', 'terminals')
        for c in clientlist:
            qstatus = "select * from status where ip=" + "\'"+clients[c]+"\'" + " order by time desc limit 1"
            statusresult = influxclient.query(qstatus)
            if statusresult:
                for sr in statusresult:
                    for s in sr:
                        conn_stat = s['connect']
                        utc_time_str = s['time']
                        utc_time = parser.parse(utc_time_str)
                        conn_time = utc_time.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                conn_stat = 'off'
                conn_time = 'NULL'

            qtemp = "select * from temperature where client=" + "\'"+c+"\'" + " order by time desc limit 1"
            tempresult = influxclient.query(qtemp)
            if tempresult:
                for tr in tempresult:
                    for t in tr:
                        client_temp = t['tempdata']
                        utc_time_str = t['time']
                        utc_time = parser.parse(utc_time_str)
                        temp_time = utc_time.now().strftime("%Y-%m-%d %H:%M:%S")
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
