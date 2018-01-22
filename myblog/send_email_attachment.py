#coding:utf-8
#encoding=utf-8

from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
import sys
from mimetypes import MimeTypes

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

param_1 = sys.argv[1]
mime = MimeTypes()
mime_type = mime.guess_type(param_1)[0]

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(param_1):
    msg = Message(subject='湖北无委卫星终端控制器备份脚本', sender='service@satelc.com', recipients=['13916838729@139.com'])
    msg.html = "<b>请查收附件。</b>"
    with app.open_resource(param_1) as fp:
        msg.attach(param_1, mime_type, fp.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

if __name__ == "__main__":
    send_email(param_1)
