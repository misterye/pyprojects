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
    clients = cur.fetchall()
    str_cn = ""
    for cn in clients:
        sql = ("""SELECT connect, create_time FROM status WHERE client = %s ORDER BY create_time DESC  LIMIT 1""", [cn[7]])
        cur.execute(*sql)
        current_status = cur.fetchone()
        msg_status = current_status[0]
        msg_status_time = current_status[1]
        msg_name = cn[1]
        if msg_status == 'on':
            replystat = "小站状态：在线<br>设备温度："
            replyname = "小站名称："+msg_name+"<br>"
            sql = ("""SELECT tempdata, create_time FROM temperature WHERE client = %s ORDER BY create_time DESC LIMIT 1""", [cn[7]])
            temp_result = cur.execute(*sql)
            if temp_result > 0:
                current_temp = cur.fetchone()
                msg_temp = current_temp[0]
                msg_temp_time = current_temp[1]
                replytemp = str(msg_temp)
                replytimemsg = "<br>获取时间："
                replytime = str(msg_temp_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
            else:
                replytemp = "无"
                replytimemsg = "<br>获取时间："
                replytime = str(msg_status_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
        elif msg_status == 'off':
            replyname = "小站名称："+msg_name+"<br>"
            replystat = "小站状态：断线"
            replytimemsg = "<br>获取时间："
            replytime = str(msg_status_time)
            replycontent = replyname+replystat+replytimemsg+replytime
        str_cn += replycontent+"<br><br>"
        statusreplytime = str(msg_status_time)
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
