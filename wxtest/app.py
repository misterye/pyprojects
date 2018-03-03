#coding:utf-8
from flask import Flask, g, request, make_response, url_for, redirect, render_template, jsonify
import time, hashlib, re, urllib2
#import xml.etree.ElementTree as ET
import sys

from wechatpy import parse_message, WeChatClient
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply
from wechatpy.events import SubscribeEvent
from flask_mysqldb import MySQL
import json
from collections import OrderedDict
import requests
import os
import glob
from influxdb import InfluxDBClient
#import ast

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')
# init MYSQL
mysql = MySQL(app)

#client = WeChatClient('wxbb4a6657207eb833', '0faa958c65817027da5d099f1256e5fd')
from secret import AppID, AppSecret
client = WeChatClient(AppID, AppSecret)
'''
client.menu.create({
    "button":[
        {
            "type":"view",
            "name":"工作日志",
            "url":"http://log.satelc.com"
        },
        {
            "type":"view",
            "name":"文档查询",
            "url":"http://doc.satelc.com"
        },
        {
            "type":"view",
            "name":"小站监控",
            "url":"http://satelc.com:8084/monitor/monitor_index"
        }
        ]
    }
)
menu = client.menu.get()
print menu
'''
def replyMsg(data):
    msg = parse_message(data)
    if msg.type == 'event' and msg.event == 'subscribe':
        reply = TextReply(message=msg)
        reply.content = 'Welcome to follow.'
        return reply.render()
    elif msg.type == 'event' and msg.event == 'unsubscribe':
        reply = TextReply(message=msg)
        reply.content = 'Goodbye.'
        return reply.render()
    elif msg.type == 'text':
        cur = mysql.connection.cursor()
        data = cur.execute("SELECT client, ip FROM terminals")
        allclients = cur.fetchall()
        client_list = []
        for c in allclients:
            client_list.append(c['client'])
        clients = {}
        for c in allclients:
            clients[c['client']] = c['ip']
        if msg.content in client_list:
            influxclient = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')
            qstatus = "select * from status where ip=" + "\'"+clients[msg.content]+"\'" + " order by time desc limit 1"
            statusresult = influxclient.query(qstatus)
            if statusresult:
                for sr in statusresult:
                    for s in sr:
                        conn_stat = s['connect']
                        #conn_time = s['time']
            else:
                conn_stat = 'off'
            msg_status = conn_stat
            if msg_status == 'on':
                replystat = "小站状态：在线\n设备温度："
                qtemp = "select * from temperature where client=" + "\'"+msg.content+"\'" + " order by time desc limit 1"
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
                            client_temp_time = local_time
                    replytemp = str(client_temp)
                    replytimemsg = "\n获取时间："
                    replytime = str(client_temp_time)
                    replycontent = replystat+replytemp+replytimemsg+replytime
                    reply = TextReply(content=replycontent, message=msg)
                    xml = reply.render()
                else:
                    replytemp = "无"
                    replycontent = replystat+replytemp
                    reply = TextReply(content=replycontent, message=msg)
                    xml = reply.render()

            elif msg_status == 'off':
                #reply = TextReply(content='小站断线', message=msg)
                replystat = "小站状态：断线"
                replycontent = replystat
                reply = TextReply(content=replycontent, message=msg)
                xml = reply.render()
            return xml
            cur.close()
        else:
            reply = TextReply(content='请输入用户终端名：', message=msg)
            xml = reply.render()
            return xml
            cur.close()
    else:
        reply = TextReply(message=msg)
        reply.content = 'Sorry, can not handle this for now.'
        return reply.render()

'''
def ordered_dict_to_xml(dict_data):
    xml_str = '<xml>'
    for key, value in dict_data.items():
        xml_str += '<%s><![CDATA[%s]]></%s>' % (key, value, key)
    xml_str += '</xml>'
    return xml_str
'''

@app.route("/")
@app.route("/homepage")
def homepage():
    return "<h1 style='color:blue'>Wechat MP test.</h1>"

# mp
@app.route('/mp')
def mp():
    return redirect(url_for('static',filename='MP_verify_2yJF2WWPOOiHbCpo.txt'))

# client_status
@app.route('/client_status')
def client_status():
    oldpath = os.getcwd()
    newpath = os.getcwd()+'/static'
    #print("The path is: %s" % newpath)
    #print("The type of newpath is: %s" % type(newpath))
    #print newpath
    os.chdir(newpath)
    #print("List files are: %s" % os.listdir(newpath))
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    #print("The new list of files are: %s" % files)
    #print files
    latest = files[-1]
    os.chdir(oldpath)
    #print("The current path is: %s" % os.getcwd())
    return redirect(url_for('static', filename=latest))

# weixin
@app.route('/wx',methods=['GET','POST'])
def wx():
    if request.method == 'GET':
        if len(request.args) > 3:
            my_signature = request.args.get('signature')
            my_timestamp = request.args.get('timestamp')
            my_nonce = request.args.get('nonce')
            my_echostr = request.args.get('echostr')
            token = 'yebin817'
            data = [token,my_timestamp,my_nonce]
            data.sort()
            temp = ''.join(data)
            mysignature = hashlib.sha1(temp).hexdigest()
            if my_signature == mysignature:
                return my_echostr
            else:
                return make_response('认证失败')
        else:
        	return '认证失败'
    elif request.method == 'POST':
        print("The request data is: %s" % request.data)
    	return replyMsg(request.data)

'''
@app.route('/getStatus', methods=['POST'])
def getStatus():
    olddict = request.json
    print olddict
    print type(olddict)

    dictdata = OrderedDict()
    dictdata["ToUserName"] = olddict["ToUserName"]
    dictdata["FromUserName"] = olddict["FromUserName"]
    dictdata["CreateTime"] = olddict["CreateTime"]
    dictdata["MsgType"] = olddict["MsgType"]
    dictdata["Content"] = olddict["Content"]
    dictdata["MsgId"] = olddict["MsgId"]

    print dictdata
    print type(dictdata)

    xml_data = ordered_dict_to_xml(dictdata)
    print xml_data
    print type(xml_data)

    #return xml_data
    return replyMsg(xml_data)
'''

if __name__ == "__main__":
    app.run('0.0.0.0', 8020)
