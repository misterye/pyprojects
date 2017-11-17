# coding=utf-8
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '840821'
app.config['MYSQL_DB'] = 'myblog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'gq49gr9jgfkw4k950wjkgjwlhfw0'
socketio = SocketIO(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('Unauthorized, Please login.', 'danger')
            flash("未授权，请先登录。", 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@is_logged_in
def index():
    return render_template('chatup.html', name = name)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            global name
            name = data['name']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['name'] = name

                #flash('You are now logged in.', 'success')
                flash("登录成功。", 'success')
                return redirect(url_for('index'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found.'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Chat
@app.route('/chat')
def chat():
    #return redirect("http://139.224.114.83:8084")
    return redirect("http://chat.satelc.com")

# Main Page
@app.route('/main')
def main():
    #return redirect("http://139.224.114.83:8019")
    return redirect("http://satelc.com")

@app.route('/terminals')
def terminals():
    #return redirect("http://139.224.114.83:8019/terminals")
    return redirect("http://satelc.com/terminals")

@app.route('/articles')
def articles():
    #return redirect("http://139.224.114.83:8019/articles")
    return redirect("http://satelc.com/articles")

@app.route('/monitor')
def monitor():
    #return redirect("http://139.224.114.83:8086/")
    return redirect("http://monitor.satelc.com/")

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("已注销。", 'success')
    return redirect(url_for('login'))

def messageReceived():
    print('Message Received!')

@socketio.on('my_event')
def handleMyevent(json):
    print('Received my event: ' + str(json))
    socketio.emit('my_response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', debug=True, port=8084)
