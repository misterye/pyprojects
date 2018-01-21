#coding:utf-8
#encoding=utf-8

import time
import requests
import json
import MySQLdb
import sys
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

def send_slack_msg(msg):
    payload = {"text": msg}
    try:
        slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

'''
def send_slack_link():
    link = "http://satelc.com:5000/client_status"
    data = requests.request("GET", link)
    newurl = data.url
    payload_url = "<%s|点击> 查看所有终端当前状态" % newurl
    #payload = {"text": "<http://satelc.com:5000/client_status|点击> 查看所有终端当前状态"}
    payload = {"text": payload_url}
    try:
        slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)
'''        

# Three "#" means accessing static files.
def send_slack_link(id):
    ### link = "http://satelc.com:5000/client_status"
    link_id = "http://satelc.com/client_status/"+str(id)+"/"
    ### data = requests.request("GET", link)
    ### newurl = data.url
    ### payload_url = "<%s|点击> 查看所有终端当前状态" % newurl
    #payload = {"text": "<http://satelc.com:5000/client_status|点击> 查看所有终端当前状态"}
    ### payload = {"text": payload_url}
    payload_url_id = "<%s|点击> 查看所有终端当前状态" % link_id
    payload_id = {"text": payload_url_id}
    try:
        ### slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload_id), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

def send_dingding_msg(msg):
    payload = { "msgtype": "text", "text": { "content": msg } }
    try:
        dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)

'''
def send_dingding_link():
    link = "http://satelc.com:5000/client_status"
    data = requests.request("GET", link)
    newurl = data.url
    #payload = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": "http://satelc.com:5000/client_status" } }
    payload = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": newurl } }
    try:
        dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except requests.RequestException as e:
        print(e.message)
'''

# Three "#" means accessing static files.
def send_dingding_link(id):
    ### link = "http://satelc.com:5000/client_status"
    link_id = "http://satelc.com/client_status/"+str(id)+"/"
    ### data = requests.request("GET", link)
    ### newurl = data.url
    #payload = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": "http://satelc.com:5000/client_status" } }
    ### payload = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": newurl } }
    payload_id = { "msgtype": "link", "link": { "text":"点击查看详情！", "title":"所有终端当前状态", "messageUrl": link_id } }
    try:
        ### dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
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
        #print(cn[7])
        sql = ("""SELECT connect, create_time FROM status WHERE client = %s ORDER BY id DESC  LIMIT 1""", [cn[7]])
        cur.execute(*sql)
        current_status = cur.fetchone()
        msg_status = current_status[0]
        msg_status_time = current_status[1]
        msg_name = cn[1]
        #msg_name = cn[7]
        #print("msg_name is: %s" % msg_name)
        if msg_status == 'on':
            #replyname = "小站名称："+msg_name+"\n"
            #replystat = "小站状态：在线\n设备温度："
            replystat = "小站状态：在线<br>设备温度："
            replyname = "小站名称："+msg_name+"<br>"
            sql = ("""SELECT tempdata, create_time FROM temperature WHERE client = %s ORDER BY id DESC LIMIT 1""", [cn[7]])
            temp_result = cur.execute(*sql)
            if temp_result > 0:
                current_temp = cur.fetchone()
                msg_temp = current_temp[0]
                msg_temp_time = current_temp[1]
                replytemp = msg_temp
                #replytimemsg = "\n获取时间："
                replytimemsg = "<br>获取时间："
                replytime = str(msg_temp_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
            else:
                replytemp = "无"
                #replytimemsg = "\n获取时间："
                replytimemsg = "<br>获取时间："
                replytime = str(msg_status_time)
                replycontent = replyname+replystat+replytemp+replytimemsg+replytime
        elif msg_status == 'off':
            #replyname = "小站名称："+msg_name+"\n"
            replyname = "小站名称："+msg_name+"<br>"
            replystat = "小站状态：断线"
            #replytimemsg = "\n获取时间："
            replytimemsg = "<br>获取时间："
            replytime = str(msg_status_time)
            replycontent = replyname+replystat+replytimemsg+replytime
        str_cn += replycontent+"<br><br>"

    # Store status of all clients into the database.
    content_title = "Status of all clients generated at "+replytime
    #print content_title
    try:
        #print "Storing status of clients in the database..."
        newsql = ("""INSERT INTO client_status(title, body) VALUES(%s, %s)""", ([content_title], [str_cn]))
        cur.execute(*newsql)
        db.commit()
    #    print "Done!"
    except:
        db.rollback()
    #    print "Failed storing status of clients in the database."

    # Fetch current status id.    
    idsql = ("""SELECT id FROM client_status WHERE title = %s""", [content_title])
    cur.execute(*idsql)
    status_id = cur.fetchone()
    current_id = status_id[0]
    #print("Current id is: %s" % current_id)
    #print("Type of current_id is: %s" % type(current_id))

    # Write a html file which contains the status of all clients to a directory.
    # Send the link of status of all clients to slack and dingding robots.

    ''' ### Disable file writing function. ###
    filename = "static/"+"client_status "+replytime+".html"
    status_file = open(filename, "w")
    status_file.write(str_cn)
    status_file.close()
    '''
#        send_slack_msg(replycontent)
#        send_dingding_msg(replycontent)
    send_slack_link(current_id)
    send_dingding_link(current_id)
    cur.close()
    db.close()
    time.sleep(3600)
