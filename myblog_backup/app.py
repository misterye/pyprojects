# coding=utf-8
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from math import ceil
from flask_socketio import SocketIO, emit

#import redis
from gevent import monkey
monkey.patch_all()
from openvpn_status import parse_status
from time import sleep
import os
import requests
import json
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
# escape from sql attack
import cgi

global perpage
perpage = 10

'''
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
'''

app = Flask(__name__)
#app.config['SECRET_KEY'] = '\xa3\xe9\r\xc3\xc2u\xc2\xf1\x05}\xa8`\x9f\x08l\xff\x05\xe6\x06\x89K&Kt'
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '840821'
app.config['MYSQL_DB'] = 'myblog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
#db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.exmail.qq.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'service@satelc.com',
    MAIL_PASSWORD = 'Bin*ping2252266'
    )
mail = Mail(app)

# Index
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

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

# Check if user is yebin
def is_yebin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'yebin':
            return f(*args, **kwargs)
        else:
            flash("操作未授权！请以管理员身份登录。", 'danger')
            return redirect(url_for('login'))
    return wrap

# Check if user is admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash("操作未授权！请以管理员身份登录。", 'danger')
            return redirect(url_for('login'))
    return wrap

# Chat
'''
@app.route('/chat')
def chat():
    #return redirect("http://139.224.114.83:8084")
    return redirect("http://chat.satelc.com")
'''
@app.route('/chat', methods=['GET', 'POST'])
@is_logged_in
def chat():
    chatname = session['name']
    return render_template('chatup.html', chatname = chatname)

def messageReceived():
    print('Message Received!')

@socketio.on('my_event')
def handleMyevent(json):
    print('Received my event: ' + str(json))
    socketio.emit('my_response', json, callback=messageReceived)

# RSSH
@app.route('/rssh')
def rssh():
    #return redirect("http://139.224.114.83:8085")
    return redirect("http://satelc.com:8085/")

# MONITOR
'''
@app.route('/monitor')
def monitor():
    #return redirect("http://139.224.114.83:8086")
    return redirect("http://monitor.satelc.com")
'''
##############################################
#@app.route('/monitor')
#def monitor():
#    return render_template('monitor.html')
    
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/getTemp', methods=['POST'])
def getTemp():
    global pidata
    temp_data = request.json
    #print('temp_data: %s' % temp_data)
    temp = temp_data['pi_temp']
    #print('temp is: %s' % temp)
    piname = temp_data['pi_name']
    #print('piname is: %s' % piname)
    pidata = piname+temp
    #print('pidata is: %s' % pidata)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO temperature (tempdata, client) VALUES (%s, %s)", (temp, piname))
    mysql.connection.commit()
    # Send email when temperature is greater than 26. 
    result = cur.execute("SELECT * FROM terminals WHERE client=%s", [piname])
    if result > 0:
        data = cur.fetchone()
        user_name = data['name']
        
        if float(temp) > 28:
            alert_msg = user_name + "：" + temp + " 摄氏度"
            slack_payload = {"text": alert_msg}
            #dingding_payload = { 'msgtype': 'text', 'text': { 'content': alert_msg }, 'at': { 'atMobiles': ['13916838729'], 'isAtAll': 0 }}
            dingding_payload = { "msgtype": "text", "text": { "content": alert_msg } }
            try:
                # Send messages to slack satellite-terminals channel.
                slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
                # Send messages to dingding robot.
                dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(dingding_payload), headers={'Content-Type': 'application/json'})
            except requests.RequestException as e:
                print(e.message)
        # Send emails to alert@satelc.com
        if float(temp) > 30:
            msg = Message(subject=user_name, sender='service@satelc.com', recipients=['alert@satelc.com'])
            msg.html = user_name + '：' + temp
            thr = Thread(target=send_async_email, args=[app, msg])
            thr.start()
    else:
        flash("无此站", 'danger')
    cur.close()
    return pidata

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@app.route('/clientstatus', defaults={'page':1})
@app.route('/clientstatus/<int:page>')
#@app.route('/monitor')
@is_logged_in
def clientstatus(page):
    with open('/home/yebin/pyprojects/myblog/vlog.log') as log:
        stat = parse_status(log.read())
    clist = stat.client_list
    print("clist is: %s" % clist)

    nclist = []
    for cli in clist:
        nclist.append(cli)
    print nclist

    if len(nclist) == 0:
        initRequest_data = {'pi_temp':'35.7', 'pi_name':'test'}
        requests.post('http://139.224.114.83:8086/getTemp', json=initRequest_data)
        
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM terminals")
    data = cur.fetchall()
    global total_num
    total_num = len(data)
    monitor_perpage = 20
    global monitor_pages
    monitor_pages = int(ceil(len(data) / float(monitor_perpage)))
    startat = (page-1)*monitor_perpage  

    # Get client from table terminals in DB
    global getclients
    def getclients():
        global display, pidata, pname
        pname = pidata[:-4]
        display = pidata[-4:]
        # Create cursor
        cur = mysql.connection.cursor()
        # Get client
        #result = cur.execute("SELECT name, ip, client, modem, satellite FROM terminals")
        result = cur.execute("SELECT name, ip, client, modem, satellite FROM terminals limit %s, %s", (startat, monitor_perpage))
        dbclients = cur.fetchall()
        global clients
        clients = []
        for dc in dbclients:
            clients.append(dc['client'])
            #print clients
        global ips
        ips = []
        for di in dbclients:
            ips.append(di['ip'])
            #print ips
        global modems
        modems = []
        for dm in dbclients:
            modems.append(dm['modem'])
            #print modems
        global satellites
        satellites = []
        for ds in dbclients:
            satellites.append(ds['satellite'])
            #print satellites
        global ccount
        ccount = len(clients)
        global names
        names = []
        for dn in dbclients:
            names.append(dn['name'])
            #print names
        cur.close()
    getclients()
    return render_template('clientstatus.html', total_num=total_num, names=names, ips=ips, clients=clients, modems=modems, satellites=satellites, ccount=ccount, display=display, page=page, monitor_pages=monitor_pages)

@socketio.on('status')
def readvlog():
    #getclients()
    while True:
        getclients()
        with open('/home/yebin/pyprojects/myblog/vlog.log') as logfile:
        #with open('/home/yebin/pyprojects/monitor/openvpn-status.log') as logfile:
            status = parse_status(logfile.read())
        newclient = status.client_list
        #print newclient
        
        '''
        for cl in clients:
            if cl in newclient:
                flag = 1
                socketio.emit('online', {
                    'nclient': cl,
                    'flag': flag
                })
                print("%s online now." % cl)
            else:
                flag = 0
                socketio.emit('online', {
                    'nclient': cl,
                    'flag': flag
                })
                print("%s not online." % cl)
        '''
        # Change Dict to List
        newclientList = []
        offlineList = []
        for cl in clients:
            if cl in newclient:
                newclientList.append(cl)
            else:
                offlineList.append(cl)
        print newclientList
        l = len(newclientList)
        #print("There are %s clients online." % l)
        socketio.emit('online', {
            'nclient': newclientList,
            'nclientlen': l,
            'tempdisplay': display,
            'pname': pname
        })
        sleep(10)


@socketio.on('newstatus')
def totalonline():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM terminals")
    data = cur.fetchall()
    allclients = []
    for d in data:
        allclients.append(d['client'])
    while True:
        with open('/home/yebin/pyprojects/myblog/vlog.log') as newlogfile:
            newstatus = parse_status(newlogfile.read())
        newallclient = newstatus.client_list

        newallclientList = []
        newofflineList = []
        on = 'on'
        off = 'off'
        for ac in allclients:
            if ac in newallclient:
                newallclientList.append(ac)
                cur.execute("INSERT INTO status (client, connect) VALUES (%s, %s)", (ac, on))
                mysql.connection.commit()
            else:
                newofflineList.append(ac)
                cur.execute("INSERT INTO status (client, connect) VALUES (%s, %s)", (ac, off))
                mysql.connection.commit()
        #print newallclientList
        newlength = len(newallclientList)
        socketio.emit('totalonline', {
            'newallclient': newallclientList,
            'newallclientlen': newlength
        })
        sleep(10)

'''
@socketio.on('connect')
def ws_conn():
    c = db.incr('connected')
    socketio.emit('msg', {'count':c})

@socketio.on('disconnect')
def ws_disconn():
    c = db.decr('connected')
    socketio.emit('msg', {'count':c})
'''
##############################################

# Articles
@app.route('/articles', defaults={'page':1})
@app.route('/articles/<int:page>')
def articles(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    data = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
        return render_template('articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg, page=page, pages=pages)

# Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    return render_template('article.html', article=article)

@app.route('/terminals', defaults={'page':1})
@app.route('/terminals/<int:page>')
@is_logged_in
def terminals(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get terminals
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC")
    data = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC limit %s, %s", (startat, perpage))
    terminals = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
        return render_template('terminals.html', terminals=terminals, page=page, pages=pages)
    else:
        msg = 'No Terminal Found'
        return render_template('terminals.html', msg=msg, page=page, pages=pages)

# Single Terminal - Modified
@app.route('/terminal/<string:id>/')
@is_logged_in
def terminal(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get article
    result = cur.execute("SELECT * FROM terminals WHERE id = %s", [id])
    terminal = cur.fetchone()
    return render_template('terminal.html', terminal=terminal)

'''
# Get Clients of Terminals
@app.route('/clients')
def clients():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get clients of terminals
    result = cur.execute("SELECT * FROM terminals")
    
    terminals = cur.fetchall()

    if result > 0:
        return render_template('clients.html', terminals=terminals)
    else:
        msg = 'No Client Assigned'
        return render_template('clients.html', msg=msg)
    # Close connection
    cur.close()
'''

# Register Form Class
class RegisterForm(Form):
    name = StringField('姓名', [validators.Length(min=1, max=50)])
    username = StringField('用户名', [validators.Length(min=4, max=25)])
    email = StringField('电子邮箱', [validators.Length(min=6, max=50)])
    password = PasswordField('密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='两次输入不匹配')
    ])
    confirm = PasswordField('确认密码')

# User Form Class
class UserForm(Form):
    name = StringField('姓名', [validators.Length(min=1, max=50)])
    username = StringField('用户名', [validators.Length(min=3, max=25)])
    email = StringField('电子邮箱', [validators.Length(min=6, max=50)])
    newPassword = PasswordField('新密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='两次输入不匹配')
    ])
    confirm = PasswordField('确认新密码')

# User Register
@app.route('/register', methods=['GET', 'POST'])
@is_admin
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        #flash('You are now registered and can log in.', 'success')
        flash("注册成功，请登录。", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

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



# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("已注销。", 'success')
    return redirect(url_for('login'))

# Terminals Dashboard
@app.route('/dashboard', defaults={'page':1})
@app.route('/dashboard<int:page>')
#@is_logged_in
@is_admin
def dashboard(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get terminals
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC")
    data = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC limit %s, %s", (startat, perpage))
    #articles = cur.fetchall()
    terminals = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
    #    return render_template('dashboard.html', articles=articles)
        return render_template('dashboard.html', terminals=terminals, page=page, pages=pages)
    else:
    #    msg = 'No Articles Found'
        msg = 'No Terminal Found'
        return render_template('dashboard.html', msg=msg, page=page, pages=pages)

# Dashboard_Users
@app.route('/dashboard_users', defaults={'page':1})
@app.route('/dashboard_users/<int:page>')
#@is_logged_in
@is_admin
def dashboard_users(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get users
    result = cur.execute("SELECT * FROM users ORDER BY id ASC")
    data = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM users ORDER BY id ASC limit %s, %s", (startat, perpage))
    #articles = cur.fetchall()
    users = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
    #    return render_template('dashboard.html', articles=articles)
        return render_template('dashboard_users.html', users=users, page=page, pages=pages)
    else:
    #    msg = 'No Articles Found'
        msg = 'No User Found'
        return render_template('dashboard_users.html', msg=msg, page=page, pages=pages)

# Dashboard_Articles
@app.route('/dashboard_articles', defaults={'page':1})
@app.route('/dashboard_articles/<int:page>')
#@is_logged_in
@is_admin
def dashboard_articles(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    data = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
        return render_template('dashboard_articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard_articles.html', msg=msg, page=page, pages=pages)

# Article Form Class
class ArticleForm(Form):
    title = StringField("标题", [validators.Length(min=1, max=200)])
    body = TextAreaField("内容", [validators.Length(min=1)])

# Terminal Form Class - Modified
class TerminalForm(Form):
    name = StringField('用户名', [validators.Length(min=1, max=255)])
    client = StringField('终端名', [validators.Length(min=1, max=50)])
    address = StringField('小站地址', [validators.Length(min=1, max=255)])
    modem = StringField('终端类型', [validators.Length(min=1, max=50)])
    ip = StringField('管理地址')
    satellite = StringField('通信卫星', [validators.Length(min=1, max=50)])
    found_date = StringField('开通日期', [validators.Length(min=1, max=50)])
    remarks = TextAreaField("备注")

# Message Form Class
class MessageForm(Form):
    body = TextAreaField('留言内容', [validators.Length(min=1, max=300)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("公告发布成功。", 'success')
        return redirect(url_for('dashboard_articles'))
    return render_template('add_article.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    # Get form
    form = ArticleForm(request.form)
    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id = %s", (title, body, id))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("公告更新成功。", 'success')
        return redirect(url_for('dashboard_articles'))
    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
#@is_logged_in
@is_admin
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash("公告删除成功。", 'success')
    return redirect(url_for('dashboard_articles'))

# Add Terminal - Modified
@app.route('/add_terminal', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def add_terminal():
    form = TerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        client = form.client.data
        address = form.address.data
        modem = form.modem.data
        ip = form.ip.data
        satellite = form.satellite.data
        found_date = form.found_date.data
        remarks = form.remarks.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO terminals(name, client, address, modem, ip, satellite, found_date, remarks) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(name, client, address, modem, ip, satellite, found_date, remarks))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("小站添加成功。", 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_terminal.html', form=form)

# Edit Terminal - Modified
@app.route('/edit_terminal/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def edit_terminal(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get terminal by id
    result = cur.execute("SELECT * FROM terminals WHERE id = %s", [id])
    terminal = cur.fetchone()
    # Get form
    form = TerminalForm(request.form)
    # Populate terminal form fields
    form.name.data = terminal['name']
    form.client.data = terminal['client']
    form.address.data = terminal['address']
    form.modem.data = terminal['modem']
    form.ip.data = terminal['ip']
    form.satellite.data = terminal['satellite']
    form.found_date.data = terminal['found_date']
    form.remarks.data = terminal['remarks']
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        client = request.form['client']
        address = request.form['address']
        modem = request.form['modem']
        ip = request.form['ip']
        satellite = request.form['satellite']
        found_date = request.form['found_date']
        remarks = request.form['remarks']
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE terminals SET name=%s, client=%s, address=%s, modem=%s, ip=%s, satellite=%s,found_date=%s, remarks=%s WHERE id = %s", (name, client, address, modem, ip, satellite, found_date,remarks, id))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("小站更新成功。", 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_terminal.html', form=form)

# Delete Terminal - Modified 
@app.route('/delete_terminal/<string:id>', methods=['POST'])
#@is_logged_in
@is_admin
def delete_terminal(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM terminals WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash("小站删除成功。", 'success')
    return redirect(url_for('dashboard'))

# Edit User
@app.route('/edit_user/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def edit_user(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get user by id
    result = cur.execute("SELECT * FROM users WHERE id = %s", [id])
    user = cur.fetchone()
    # Get user
    form = UserForm(request.form)
    # Populate user form fields
    form.name.data = user['name']
    form.username.data = user['username']
    form.email.data = user['email']
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = sha256_crypt.encrypt(str(request.form['newPassword']))
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE users SET name=%s, username=%s, email=%s, password=%s WHERE id = %s", (name, username, email, password, id))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("用户更新成功。", 'success')
        return redirect(url_for('dashboard_users'))
    return render_template('edit_user.html', form=form)

# Delete User 
@app.route('/delete_user/<string:id>', methods=['POST'])
#@is_logged_in
@is_admin
def delete_user(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash("用户删除成功。", 'success')
    return redirect(url_for('dashboard_users'))

# Messages
@app.route('/messages', methods=['GET', 'POST'])
@is_logged_in
# @is_yebin
def messages():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get messages
    result = cur.execute("SELECT * FROM messages ORDER BY create_date DESC")
    messages = cur.fetchall()
    if result > 0:
        return render_template('messages.html', messages=messages)
    else:
        msg = 'no messages found'
        return render_template('messages.html', msg=msg)
    # Close connection
    cur.close()

# Post A Message
@app.route('/post_message', methods=['GET', 'POST'])
@is_logged_in
def post_message():
    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages(body, author) VALUES(%s, %s)", (body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash("留言已发布。", 'success')
        return redirect(url_for('messages'))
    return render_template('post_message.html', form=form)

# Delete A Message
@app.route('/delete_message/<string:id>', methods=['POST'])
#@is_logged_in
@is_admin
def delete_message(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM messages WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    flash("留言已删除。", 'success')
    return redirect(url_for('messages'))
###############################################

# Search
# Search Terminal Form Class
class SearchTerminalForm(Form):
    keyword = StringField('站内查询', [validators.Length(min=1, max=30)])

# Search Terminal Form of Keyword
@app.route('/search_keyword')
@is_logged_in
def search_keyword():
    form = SearchTerminalForm(request.form)
    return render_template('search_terminal_form.html', form=form)

# Search Terminal By Name
@app.route('/search_terminal_name', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_name/<int:page>', methods=['GET','POST'])
def search_terminal_name(page):
    urlstr = 'search_terminal_name'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE name LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE name LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Client
@app.route('/search_terminal_client', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_client/<int:page>', methods=['GET','POST'])
def search_terminal_client(page):
    urlstr = 'search_terminal_client'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE client LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE client LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Address
@app.route('/search_terminal_address', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_address/<int:page>', methods=['GET','POST'])
def search_terminal_address(page):
    urlstr = 'search_terminal_address'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE address LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE address LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Modem
@app.route('/search_terminal_modem', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_modem/<int:page>', methods=['GET','POST'])
def search_terminal_modem(page):
    urlstr = 'search_terminal_modem'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE modem LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE modem LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Satellite
@app.route('/search_terminal_satellite', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_satellite/<int:page>', methods=['GET','POST'])
def search_terminal_satellite(page):
    urlstr = 'search_terminal_satellite'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE satellite LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE satellite LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By IP
@app.route('/search_terminal_ip', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_ip/<int:page>', methods=['GET','POST'])
def search_terminal_ip(page):
    urlstr = 'search_terminal_ip'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE ip LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE ip LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Found_Date
@app.route('/search_terminal_found_date', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_found_date/<int:page>', methods=['GET','POST'])
def search_terminal_found_date(page):
    urlstr = 'search_terminal_found_date'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE found_date LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE found_date LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Terminal By Remarks
@app.route('/search_terminal_remarks', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_terminal_remarks/<int:page>', methods=['GET','POST'])
def search_terminal_remarks(page):
    urlstr = 'search_terminal_remarks'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM terminals WHERE remarks LIKE (%s) ORDER BY id ASC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM terminals WHERE remarks LIKE (%s) ORDER BY id ASC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_terminal_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_terminal_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Article By Author
@app.route('/search_article_author', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_author/<int:page>', methods=['GET','POST'])
def search_article_author(page):
    urlstr = 'search_article_author'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM articles WHERE author LIKE (%s) ORDER BY id DESC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE author LIKE (%s) ORDER BY id DESC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_article_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Article By Title
@app.route('/search_article_title', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_title/<int:page>', methods=['GET','POST'])
def search_article_title(page):
    urlstr = 'search_article_title'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM articles WHERE title LIKE (%s) ORDER BY id DESC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE title LIKE (%s) ORDER BY id DESC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_article_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Article By Body
@app.route('/search_article_body', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_body/<int:page>', methods=['GET','POST'])
def search_article_body(page):
    urlstr = 'search_article_body'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM articles WHERE body LIKE (%s) ORDER BY id DESC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE body LIKE (%s) ORDER BY id DESC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_article_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Article By Create Date
@app.route('/search_article_create_date', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_create_date/<int:page>', methods=['GET','POST'])
def search_article_create_date(page):
    urlstr = 'search_article_create_date'
    global keyword
    form = SearchTerminalForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        # escape from sql attack
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM articles WHERE create_date LIKE (%s) ORDER BY id DESC", [keyword])
    results = cur.fetchall()
    #perpage = 5
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE create_date LIKE (%s) ORDER BY id DESC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:
        msg = 'No Terminal Found'
        return render_template('search_article_result.html', msg=msg, page=page, pages=pages, urlstr=urlstr)
    cur.close()
    return render_template('search_article_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
###########################################

# Fetch the status of all the clients.
    # All Clients Status
@app.route('/all_clients_status', defaults={'page':1})
@app.route('/all_clients_status/<int:page>')
def all_clients_status(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get all clients status
    result = cur.execute("SELECT * FROM client_status")
    data = cur.fetchall()
    newperpage = 50
    pages = int(ceil(len(data) / float(newperpage)))
    startat = (page-1)*newperpage
    result = cur.execute("SELECT * FROM client_status ORDER BY id DESC limit %s, %s", (startat, newperpage))
    all_clients_status = cur.fetchall()
    # Close connection
    cur.close()
    if result > 0:
        return render_template('all_clients_status.html', all_clients_status=all_clients_status, page=page, pages=pages)
    else:
        msg = 'No clients status found.'
        return render_template('all_clients_status.html', msg=msg, page=page, pages=pages)

################################################
    # Single Client Status
@app.route('/client_status/<string:id>/')
def client_status(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get single client status
    result = cur.execute("SELECT * FROM client_status WHERE id = %s", [id])
    client_status = cur.fetchone()
    return render_template('client_status.html', client_status=client_status)

if __name__ == '__main__':
    app.secret_key = '\xa3\xe9\r\xc3\xc2u\xc2\xf1\x05}\xa8`\x9f\x08l\xff\x05\xe6\x06\x89K&Kt'
    #app.run('0.0.0.0', 8019)
    socketio.run(app, '0.0.0.0', debug=True, port=8019)
