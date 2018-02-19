# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
from project.app import app, socketio

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 8084)
