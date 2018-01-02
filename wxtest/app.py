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
#import ast

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
#app.config.from_object('config')

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '840821'
app.config['MYSQL_DB'] = 'myblog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

client = WeChatClient('wxbb4a6657207eb833', '0faa958c65817027da5d099f1256e5fd')
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
            "url":"http://monitor.satelc.com"
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
        data = cur.execute("SELECT client FROM terminals")
        client_name = cur.fetchall()
        client_list = []
        for cn in client_name:
            client_list.append(cn['client'])
        if msg.content in client_list:
            status_result = cur.execute("SELECT connect, create_time FROM status WHERE client = %s ORDER BY id DESC  LIMIT 1", [msg.content])
            current_status = cur.fetchone()
            msg_status = current_status['connect']
            msg_status_time = current_status['create_time']
            if msg_status == 'on':
                replystat = "小站状态：在线\n设备温度："
                temp_from_server_db = cur.execute("SELECT client FROM temperature")
                temp_client_server_db = cur.fetchall()
                temp_client_server_db_list = []
                for tl in temp_client_server_db:
                    temp_client_server_db_list.append(tl['client'])
                if msg.content in temp_client_server_db_list:
                    temp_result = cur.execute("SELECT tempdata, create_time FROM temperature WHERE client = %s ORDER BY id DESC LIMIT 1", [msg.content])
                    current_temp = cur.fetchone()
                    msg_temp = current_temp['tempdata']
                    msg_temp_time = current_temp['create_time']
                    #reply = TextReply(content='小站在线', message=msg)
                    replytemp = msg_temp
                    replytimemsg = "\n获取时间："
                    replytime = str(msg_temp_time)
                    replycontent = replystat+replytemp+replytimemsg+replytime
                    reply = TextReply(content=replycontent, message=msg)
                    xml = reply.render()
                else:
                    replytemp = "无"
                    replytimemsg = "\n获取时间："
                    replytime = str(msg_status_time)
                    replycontent = replystat+replytemp+replytimemsg+replytime
                    reply = TextReply(content=replycontent, message=msg)
                    xml = reply.render()

            elif msg_status == 'off':
                #reply = TextReply(content='小站断线', message=msg)
                replystat = "小站状态：断线"
                replytimemsg = "\n获取时间："
                replytime = str(msg_status_time)
                replycontent = replystat+replytimemsg+replytime
                reply = TextReply(content=replycontent, message=msg)
                xml = reply.render()
            return xml
            cur.close()
        else:
            reply = TextReply(content='请输入用户终端名：', message=msg)
            xml = reply.render()
            return xml
            cur.close()
        #cur.close()
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
    app.run(host='0.0.0.0',debug=True)
