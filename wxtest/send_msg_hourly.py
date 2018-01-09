#coding:utf-8
#encoding=utf-8

import time
import requests
import json
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def send_slack_msg(msg):
    payload = {"text": msg}
    try:
        slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

def send_dingding_msg(msg):
    payload = { "msgtype": "text", "text": { "content": msg } }
    try:
        dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

while True:
    db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog", charset="utf8")
    cur = db.cursor()
    cur.execute("""SELECT * FROM terminals""")
    clients = cur.fetchall()
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
            replyname = "小站名称："+msg_name+"\n"
            replystat = "小站状态：在线\n设备温度："
            sql = ("""SELECT tempdata, create_time FROM temperature WHERE client = %s ORDER BY id DESC LIMIT 1""", [cn[7]])
            temp_result = cur.execute(*sql)
            if temp_result > 0:
                current_temp = cur.fetchone()
                msg_temp = current_temp[0]
                msg_temp_time = current_temp[1]
                replytemp = msg_temp
                replytimemsg = "\n获取时间："
                replytime = str(msg_temp_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
            else:
                replytemp = "无"
                replytimemsg = "\n获取时间："
                replytime = str(msg_status_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
        elif msg_status == 'off':
            replyname = "小站名称："+msg_name+"\n"
            replystat = "小站状态：断线"
            replytimemsg = "\n获取时间："
            replytime = str(msg_status_time)
            replycontent = replyname+replystat+replytimemsg+replytime
        send_slack_msg(replycontent)
        send_dingding_msg(replycontent)
    cur.close()
    time.sleep(1800)