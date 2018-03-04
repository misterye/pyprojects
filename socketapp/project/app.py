# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";

from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
#from flask_mail import Mail
#from flask_mail import Message
#from threading import Thread
import os

socketio = SocketIO()

"""Create an application."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')
db = MySQL(app)
#mail = Mail(app)

def memoryUsage():
    # server memory usage
    os.system('free -h > /home/yebin/pyprojects/myblog/memuse')
    f = open('/home/yebin/pyprojects/myblog/memuse', 'r')
    lines = f.readlines()
    linestring = lines[1].split()
    totalstr = linestring[1]
    usedstr = linestring[2]
    freestr = linestring[3]
    sharedstr = linestring[4]
    buffstr = linestring[5]
    availablestr = linestring[6]
    memstr = "total: " + totalstr + " | " + "used: " + usedstr + " | " + "free: " + freestr + " | " + "shared: " + sharedstr + " | " + "buff/cache: " + buffstr + " | " + "available: " + availablestr
    return memstr

from .chat import chat_blueprint
from .monitor import monitor_blueprint

app.register_blueprint(chat_blueprint, url_prefix='/chat')
app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

socketio.init_app(app)


