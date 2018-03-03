# -*- coding: utf-8 -*-
import time
import requests
import json
import MySQLdb
import sys
import urllib2

from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
from influxdb import InfluxDBClient

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')

mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_slack_link(id):
    link_id = "http://satelc.com/client_status/"+str(id)+"/"
    payload_url_id = "<%s|点击> 查看所有终端当前状态" % link_id
    payload_id = {"text": payload_url_id}
    try:
        slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload_id), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

def send_dingding_link(id):
    link_id = "http://satelc.com/client_status/"+str(id)+"/"
    payload_id = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": link_id } }
    try:
        dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(payload_id), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

while True:
    db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog", charset="utf8")
    cur = db.cursor()
    cur.execute("""SELECT * FROM terminals""")
    allclients = cur.fetchall()
    clientlist = []
    for c in allclients:
        clientlist.append(c[7])
    clients = {}
    for c in allclients:
        clients[c[7]] = c[4]
    str_cn = ""
    influxclient = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')
    for c in allclients:
        qstatus = "select * from status where ip=" + "\'"+clients[c[7]]+"\'" + " order by time desc limit 1"
        statusresult = influxclient.query(qstatus)
        if statusresult:
            for sr in statusresult:
                for s in sr:
                    conn_stat = s['connect']
                    conn_time = s['time']
        else:
            conn_stat = 'off'    
        msg_name = c[1]
        if conn_stat == 'on':
            replystat = "小站状态：在线<br>设备温度："
            replyname = "小站名称："+msg_name+"<br>"
            qtemp = "select * from temperature where client=" + "\'"+c[7]+"\'" + " order by time desc limit 1"
            tempresult = influxclient.query(qtemp)
            if tempresult:
                for tr in tempresult:
                    for t in tr:
                        client_temp = t['tempdata']
                        client_temp_time = t['time']
                replytemp = str(client_temp)
                replytime = str(client_temp_time)
                replytimemsg = "<br>获取时间："
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
            else:
                client_temp = 99.9
                replytemp = "无"
                replytimemsg = "<br>获取时间："
                replytime = str(conn_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
        elif conn_stat == 'off':
            replyname = "小站名称："+msg_name+"<br>"
            replystat = "小站状态：断线"
            replycontent = replyname+replystat
        str_cn += replycontent+"<br><br>"
        statusreplytime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    content_title = "Status of All Clients @ "+statusreplytime
    msg = Message(subject='卫星终端控制器状态', sender='service@satelc.com', recipients=['13916838729@139.com'])
    msg.html = str_cn
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    try:
        newsql = ("""INSERT INTO client_status(title, body) VALUES(%s, %s)""", ([content_title], [str_cn]))
        cur.execute(*newsql)
        db.commit()
    except:
        db.rollback()

    idsql = ("""SELECT id FROM client_status WHERE title = %s""", [content_title])
    cur.execute(*idsql)
    status_id = cur.fetchone()
    current_id = status_id[0]

    send_slack_link(current_id)
    send_dingding_link(current_id)

    cur.close()
    db.close()
    time.sleep(3600)
