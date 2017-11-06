#coding:utf-8
from flask import Flask, g, request, make_response, url_for, redirect, render_template
import time, hashlib, re
import xml.etree.ElementTree as ET
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
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
    else:
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
