# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
from flask import session
from flask_socketio import emit, join_room, leave_room
from ..app import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'name': session.get('name') + ' 进入' + room + '。'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    #print("用户组为：%s" % room)
    #print("消息为：%s" % message['msg'].encode("latin-1","ignore"))
    #print("消息类型为：%s" % type(message['msg']))
    emit('message', {'name': session.get('name'), 'msg': message['msg'].encode("latin-1","ignore")}, room=room)

@socketio.on('broadcast_text', namespace='/chat')
def broadcast_text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    #room = session.get('room')
    emit('message', {'name': session.get('name'), 'msg': message['msg'].encode("latin-1","ignore")}, broadcast=True)

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'name': session.get('name') + ' 离开' + room +'。'}, room=room)

@socketio.on('my_ping', namespace='/chat')
def ping_pong():
    emit('my_pong')

'''
@socketio.on('my_event', namespace='/chat')
def my_event(message):
    emit('my_response', message)

@socketio.on('my_ping', namespace='/chat')
def ping_pong():
    emit('my_pong')
'''