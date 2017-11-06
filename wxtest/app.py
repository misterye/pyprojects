from flask import Flask, g, request, make_response, url_for, redirect
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

def recv_msg(oriData):
    xmldata = ET.fromstring(oriData)
    fromusername = xmldata.find("FromUserName").text
    tousername = xmldata.find("ToUserName").text
    content = xmldata.find("Content").text
    xmldict = {"FromUserName": fromusername,"ToUserName": tousername, "Content": content}
    return xmldict

def submit_msg(content_dict={"": ""}, type="text"):
    toname = content_dict["FromUserName"]
    fromname = content_dict["ToUserName"]
    content = content_dict["Content"]
    content = "Yes, %s, and?" % (content)
    reply = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>
        """
    resp_str = reply % (toname, fromname, int(time.time()), content)
    return resp_str

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
