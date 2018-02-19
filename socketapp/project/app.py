# coding=utf-8
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

socketio = SocketIO()

"""Create an application."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')
db = MySQL(app)

from .chat import chat_blueprint
#from project.monitor import monitor_blueprint

app.register_blueprint(chat_blueprint)
#app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

socketio.init_app(app)


