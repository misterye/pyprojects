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
from ..app import socketio
from ..app import db
#from time import sleep

@socketio.on('my_event', namespace='/monitor')
def my_event(msg):
    emit('my_response', msg)

@socketio.on('status', namespace='/monitor')
def clientStatus():
    cur = db.connection.cursor()
    cur.execute("SELECT client FROM terminals")
    allclients = cur.fetchall()
    clients = []
    for dc in allclients:
        clients.append(dc['client'])
    #print("数据库中所有小站：%s" % clients)
    while True:
        for c in clients:
            cur.execute("SELECT client, connect FROM status WHERE client=%s ORDER BY ID DESC LIMIT 1", [c])
            client = cur.fetchone()
            #print("小站名称：%s" % client['client'])
            #print("小站状态：%s" % client['connect'])
            emit('online', {
                'client_name': client['client'],
                'client_status': client['connect']
                })
        #socketio.sleep(10)
        eventlet.sleep(10)