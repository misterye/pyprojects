#coding:utf-8
from flask import Flask, g, request, make_response, url_for, redirect, render_template
import time, hashlib, re, urllib2
#import xml.etree.ElementTree as ET
import sys

from wechatpy import parse_message, WeChatClient
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply
from wechatpy.events import SubscribeEvent
from flask_mysqldb import MySQL

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
            result = cur.execute("SELECT connect FROM status WHERE client = %s ORDER BY id DESC  LIMIT 1", [msg.content])
            current_status = cur.fetchone()
            msg_status = current_status['connect']
            if msg_status == 'on':
                reply = TextReply(content='小站在线', message=msg)
                xml = reply.render()
            elif msg_status == 'off':
                reply = TextReply(content='小站断线', message=msg)
                xml = reply.render()
            return xml
        else:
            reply = TextReply(content='请输入用户终端名：', message=msg)
            xml = reply.render()
            return xml
        cur.close()
    else:
        reply = TextReply(message=msg)
        reply.content = 'Sorry, can not handle this for now.'
        return reply.render()

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
    	return replyMsg(request.data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
