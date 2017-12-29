# coding=utf-8
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";

from gevent import monkey
monkey.patch_all()

import redis
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_socketio import SocketIO, emit
from openvpn_status import parse_status
from time import sleep
from math import ceil
import os
import requests

from flask_mysqldb import MySQL

app = Flask(__name__)

db = redis.StrictRedis('localhost', 6379, 0)
app.config['SECRET_KEY'] = 'fiaeg7afe9adfhaofhd4rdgha0r'
socketio = SocketIO(app)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '840821'
app.config['MYSQL_DB'] = 'myblog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

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

# home page
@app.route('/')
def home():
    return render_template('home.html')

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
    cur.close()
    return pidata

@app.route('/clientstatus', defaults={'page':1})
@app.route('/clientstatus/<int:page>')
#@app.route('/monitor')
@is_logged_in
def clientstatus(page):
    with open('/home/yebin/pyprojects/monitor/vlog.log') as log:
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
    perpage = 20
    global pages
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage  

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
        result = cur.execute("SELECT name, ip, client, modem, satellite FROM terminals limit %s, %s", (startat, perpage))
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
    return render_template('clientstatus.html', total_num=total_num, names=names, ips=ips, clients=clients, modems=modems, satellites=satellites, ccount=ccount, display=display, page=page, pages=pages)

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

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                #flash('You are now logged in.', 'success')
                flash("登录成功。", 'success')
                return redirect(url_for('monitor'))
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

@socketio.on('status')
def readvlog():
    #getclients()
    while True:
    	getclients()
        with open('/home/yebin/pyprojects/monitor/vlog.log') as logfile:
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
        with open('/home/yebin/pyprojects/monitor/vlog.log') as newlogfile:
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


@socketio.on('connect')
def ws_conn():
    c = db.incr('connected')
    socketio.emit('msg', {'count':c})

@socketio.on('disconnect')
def ws_disconn():
    c = db.decr('connected')
    socketio.emit('msg', {'count':c})

#@socketio.on('client')
#def ws_client(json):
#    socketio.emit('online', json)

@app.route('/index')
def index():
    #return redirect("http://139.224.114.83:8019/")
    return redirect("http://satelc.com/")

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

#@app.route('/login')
#def login():
#    return redirect("http://139.224.114.83:8019/login")

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', debug=True, port=8086)
