#coding:utf-8
#encoding=utf-8

from flask import Flask
import time
import requests
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.debug = True

app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.exmail.qq.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'service@satelc.com',
    MAIL_PASSWORD = 'Bin*ping2252266'
    )

mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
while True:
    db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog", charset="utf8")
    cur = db.cursor()
    cur.execute("""SELECT * FROM terminals""")
    clients = cur.fetchall()
    str_cn = ""
    for cn in clients:
        print(cn[7])
        sql = ("""SELECT connect, create_time FROM status WHERE client = %s ORDER BY id DESC  LIMIT 1""", [cn[7]])
        cur.execute(*sql)
        current_status = cur.fetchone()
        msg_status = current_status[0]
        msg_status_time = current_status[1]
        msg_name = cn[1]
        #msg_name = cn[7]
        print("msg_name is: %s" % msg_name)
        if msg_status == 'on':
            replyname = "小站名称："+msg_name+"<br>"
            replystat = "小站状态：在线<br>设备温度："
            sql = ("""SELECT tempdata, create_time FROM temperature WHERE client = %s ORDER BY id DESC LIMIT 1""", [cn[7]])
            temp_result = cur.execute(*sql)
            if temp_result > 0:
                current_temp = cur.fetchone()
                msg_temp = current_temp[0]
                msg_temp_time = current_temp[1]
                replytemp = msg_temp
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
    msg = Message(subject='卫星终端控制器状态', sender='service@satelc.com', recipients=['13916838729@139.com'])
    msg.html = str_cn
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    cur.close()
    time.sleep(3600)
