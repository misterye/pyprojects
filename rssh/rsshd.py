#!/home/yebin/pyprojects/rssh/.venv/bin/python

from gevent import monkey
monkey.patch_all()

from flask import Flask, request, abort, render_template, redirect
from werkzeug.exceptions import BadRequest
import gevent
import rssh


app = Flask(__name__)


@app.route('/')
@app.route('/rssh')
def index():
    return render_template('index.html')

'''
@app.route('/home')
def home():
    return redirect("http://139.224.114.83:8019/")

@app.route('/terminals')
def terminals():
    return redirect("http://139.224.114.83:8019/terminals")

@app.route('/articles')
def articles():
    return redirect("http://139.224.114.83:8019/articles")

@app.route('/monitor')
def monitor():
    return redirect("http://139.224.114.83:8086/")
	
@app.route('/login')
def login():
    return redirect("http://139.224.114.83:8019/login")
'''	

@app.route('/rssh/<hostname>/<username>')
def connect(hostname, username):
    app.logger.debug('{remote} -> {username}@{hostname}: {command}'.format(
            remote=request.remote_addr,
            username=username,
            hostname=hostname,
            command=request.args['run'] if 'run' in request.args else
                '[interactive shell]'
        ))

    # Abort if this is not a websocket request
    if not request.environ.get('wsgi.websocket'):
        app.logger.error('Abort: Request is not WebSocket upgradable')
        raise BadRequest()

    bridge = rssh.RSSHBridge(request.environ['wsgi.websocket'])
    try:
        bridge.open(
            hostname=hostname,
            username=username,
            password=request.args.get('password'),
            port=int(request.args.get('port')),
            private_key=request.args.get('private_key'),
            key_passphrase=request.args.get('key_passphrase'),
            allow_agent=app.config.get('RSSH_ALLOW_SSH_AGENT', False))
    except Exception as e:
        app.logger.exception('Error while connecting to {0}: {1}'.format(
            hostname, e.message))
        request.environ['wsgi.websocket'].close()
        return str()
    if 'run' in request.args:
        bridge.execute(request.args.get('run'))
    else:
        bridge.shell()

    # We have to manually close the websocket and return an empty response,
    # otherwise flask will complain about not returning a response and will
    # throw a 500 at our websocket client
    request.environ['wsgi.websocket'].close()
    return str()


if __name__ == '__main__':
    import argparse
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    from jinja2 import FileSystemLoader
    import os

    root_path = os.path.dirname(rssh.__file__)
    app.jinja_loader = FileSystemLoader(os.path.join(root_path, 'templates'))
    app.static_folder = os.path.join(root_path, 'static')

    parser = argparse.ArgumentParser(
        description='rsshd - SSH Over WebSockets Daemon')

    parser.add_argument('--port', '-p',
        type=int,
        default=8085,
        help='Port to bind (default: 8085)')

    parser.add_argument('--host', '-H',
        default='0.0.0.0',
        help='Host to listen to (default: 0.0.0.0)')

    parser.add_argument('--allow-agent', '-A',
        action='store_true',
        default=False,
        help='Allow the use of the local (where rsshd is running) ' \
            'ssh-agent to authenticate. Dangerous.')

    args = parser.parse_args()

    app.config['RSSH_ALLOW_SSH_AGENT'] = args.allow_agent

    agent = 'rsshd/{0}'.format(rssh.__version__)

    print '{0} running on {1}:{2}'.format(agent, args.host, args.port)

    #app.debug = True
    app.debug = False
    http_server = WSGIServer((args.host, args.port), app,
        log=None,
        handler_class=WebSocketHandler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
