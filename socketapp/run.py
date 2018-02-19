from project.app import app, socketio

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 8084)
