# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
from flask import render_template, flash, redirect, url_for, session, request
from passlib.hash import sha256_crypt
from functools import wraps
from . import chat_blueprint
from .forms import LoginForm
from ..app import db

# Login
@chat_blueprint.route('/chat_login', methods=['GET', 'POST'])
def chat_login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = db.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            global name
            name = data['name']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['name'] = name
                #flash("登录成功。", 'success')
                return redirect(url_for('.chat_index'))
            else:
                error = 'Invalid login'
                return render_template('chat_login.html', error=error)
            cur.close()
        else:
            error = 'Username not found.'
            return render_template('chat_login.html', error=error)
    return render_template('chat_login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("未授权，请先登录。", 'danger')
            return redirect(url_for('.chat_login'))
    return wrap

'''
# Home Page: Join Room
@chat_blueprint.route('/', methods=['GET', 'POST'])
@is_logged_in
def chat_index():
    """Login form to enter a room."""
    form = LoginForm()
    cur = db.connection.cursor()
    result = cur.execute("SELECT usergroup FROM users WHERE username = %s", [session['username']])
    if result > 0:
        data = cur.fetchone()
        usergroup = data['usergroup']
    else:
        usergroup = 'public'
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        if usergroup == 'test':
            session['room'] = '测试频道'
            form.room.data = session['room']
        elif usergroup == 'admin':
            session['room'] = '管理员频道'
            form.room.data = session['room']
        else:
            session['room'] = '公共频道'
            form.room.data = session['room']
            #form.room.data = session.get('room', '')
    return render_template('chat_index.html', form=form)
'''

# Home Page: Join Room
@chat_blueprint.route('/', methods=['GET', 'POST'])
@is_logged_in
def chat_index():
    """Login form to enter a room."""
    form = LoginForm()
    cur = db.connection.cursor()
    result = cur.execute("SELECT usergroup FROM users WHERE username = %s", [session['username']])
    if result > 0:
        data = cur.fetchone()
        usergroup = data['usergroup']
    else:
        usergroup = 'public'
    if request.method == 'GET':
        form.name.data = session.get('name', '')
        if usergroup == 'test':
            session['room'] = '测试组'
            form.room.data = session['room']
        elif usergroup == 'admin':
            session['room'] = '管理员组'
            form.room.data = session['room']
        else:
            session['room'] = '公共组'
            form.room.data = session['room']
    else:
        if form.validate_on_submit():
            session['name'] = form.name.data
            session['room'] = form.room.data
            return redirect(url_for('.chat'))
    return render_template('chat_index.html', form=form)


@chat_blueprint.route('/chat', methods=['GET', 'POST'])
@is_logged_in
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.chat_index'))
    return render_template('chat.html', name=name, room=room)

# Logout
@chat_blueprint.route('/chat_logout')
@is_logged_in
def chat_logout():
    session.clear()
    flash("已注销。", 'success')
    return redirect(url_for('.chat_login'))

##############################################################
# SatelC Home
@chat_blueprint.route('/home')
def home():
    return redirect("http://satelc.com/")

# Articles
@chat_blueprint.route('/articles')
def articles():
    return redirect("http://satelc.com/articles")

# Terminals
@chat_blueprint.route('/terminals')
def terminals():
    return redirect("http://satelc.com/terminals")

@chat_blueprint.route('/navmonitor')
def navmonitor():
    return redirect("http://satelc.com:8084/monitor/monitor_index")

@chat_blueprint.route('/navchat')
def navchat():
    return redirect("http://satelc.com:8084/chat/chat")

@chat_blueprint.route('/navlogout')
def navlogout():
    return redirect("http://satelc.com:8084/chat/chat_logout")

@chat_blueprint.route('/navlogin')
def navlogin():
    return redirect("http://satelc.com:8084/chat/chat_login")

# Messages
@chat_blueprint.route('/messages')
def messages():
    return redirect("http://satelc.com/messages")

# Dashboard
@chat_blueprint.route('/dashboard')
def dashboard():
    return redirect("http://satelc.com/dashboard")

# Dashboard_articles
@chat_blueprint.route('/dashboard_articles')
def dashboard_articles():
    return redirect("http://satelc.com/dashboard_articles")

# Dashboard_users
@chat_blueprint.route('/dashboard_users')
def dashboard_users():
    return redirect("http://satelc.com/dashboard_users")

# RSSH
@chat_blueprint.route('/rssh')
def rssh():
    return redirect("http://satelc.com:8085/")

# Search_keyword
@chat_blueprint.route('/search_keyword')
def search_keyword():
    return redirect("http://satelc.com/search_keyword")