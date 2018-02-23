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
from . import monitor_blueprint
from ..app import db
#from ..app import mail

# Login
@monitor_blueprint.route('/monitor_login', methods=['GET', 'POST'])
def monitor_login():
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
                flash("登录成功。", 'success')
                return redirect(url_for('.monitor_index'))
            else:
                error = 'Invalid login'
                return render_template('monitor_login.html', error=error)
            cur.close()
        else:
            error = 'Username not found.'
            return render_template('monitor_login.html', error=error)
    return render_template('monitor_login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("未授权，请先登录。", 'danger')
            return redirect(url_for('.monitor_login'))
    return wrap

'''
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
'''

'''
@monitor_blueprint.route('/getTemp', methods=['POST'])
def getTemp():
    temp_data = request.json
    pitemp = temp_data['pi_temp']
    piname = temp_data['pi_name']
    pidata = piname + pitemp
    cur = db.connection.cursor()
    cur.execute("INSERT INTO temperature (tempdata, client) VALUES (%s, %s)", (pitemp, piname))
    db.connection.commit()
    if float(pitemp) > 30:
        alert_msg = piname + "：" + pitemp + " 摄氏度"
        slack_payload = {"text": alert_msg}
        dingding_payload = { "msgtype": "text", "text": { "content": alert_msg } }
        try:
            slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
            dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(dingding_payload), headers={'Content-Type': 'application/json'})
        except requests.RequestException as e:
            print(e.message)
    if float(pitemp) > 33:
        msg = Message(subject=piname, sender='service@satelc.com', recipients=['alert@satelc.com'])
        msg.html = piname + '：' + pitemp
        thr = Thread(target=send_async_email, args=[monitor_blueprint, msg])
        thr.start()
    return pidata
'''

@monitor_blueprint.route('/monitor_index', methods=['GET', 'POST'])
@is_logged_in
def monitor_index():
    cur = db.connection.cursor()
    cur.execute("SELECT name, ip, client, modem, satellite FROM terminals")
    dbclients = cur.fetchall()
    clients = []
    for dc in dbclients:
        clients.append(dc['client'])
    ips = []
    for di in dbclients:
        ips.append(di['ip'])
    modems = []
    for dm in dbclients:
        modems.append(dm['modem'])
    satellites = []
    for ds in dbclients:
        satellites.append(ds['satellite'])
    names = []
    for dn in dbclients:
        names.append(dn['name'])
    ccount = len(clients)
    cur.close()
    return render_template('monitor_index.html', names=names, ips=ips, clients=clients, modems=modems, satellites=satellites, ccount=ccount)

# Logout
@monitor_blueprint.route('/monitor_logout')
@is_logged_in
def monitor_logout():
    session.clear()
    flash("已注销。", 'success')
    return redirect(url_for('.monitor_login'))

# SatelC Home
@monitor_blueprint.route('/home')
def home():
    return redirect("http://satelc.com/")

# Articles
@monitor_blueprint.route('/articles')
def articles():
    return redirect("http://satelc.com/articles")

# Terminals
@monitor_blueprint.route('/terminals')
def terminals():
    return redirect("http://satelc.com/terminals")

@monitor_blueprint.route('/navmonitor')
def navmonitor():
    return redirect("http://satelc.com:8084/monitor/monitor_index")

@monitor_blueprint.route('/navchat')
def navchat():
    return redirect("http://satelc.com:8084/chat/chat")

@monitor_blueprint.route('/navlogout')
def navlogout():
    return redirect("http://satelc.com:8084/monitor/monitor_logout")

@monitor_blueprint.route('/navlogin')
def navlogin():
    return redirect("http://satelc.com:8084/monitor/monitor_login")

# Messages
@monitor_blueprint.route('/messages')
def messages():
    return redirect("http://satelc.com/messages")

# Dashboard
@monitor_blueprint.route('/dashboard')
def dashboard():
    return redirect("http://satelc.com/dashboard")

# Dashboard_articles
@monitor_blueprint.route('/dashboard_articles')
def dashboard_articles():
    return redirect("http://satelc.com/dashboard_articles")

# Dashboard_users
@monitor_blueprint.route('/dashboard_users')
def dashboard_users():
    return redirect("http://satelc.com/dashboard_users")

# RSSH
@monitor_blueprint.route('/rssh')
def rssh():
    return redirect("http://satelc.com:8085/")

# Search_keyword
@monitor_blueprint.route('/search_keyword')
def search_keyword():
    return redirect("http://satelc.com/search_keyword")