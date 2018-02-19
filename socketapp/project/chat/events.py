from flask import session
from flask_socketio import emit, join_room, leave_room
from ..app import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)

@socketio.on('broadcast_text', namespace='/chat')
def broadcast_text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    #room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, broadcast=True)

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

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