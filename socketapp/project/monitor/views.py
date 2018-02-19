

socketio = SocketIO(app)
mail = Mail(app)

def messageReceived():
    print('Message Received!')

@socketio.on('my_event')
def handleMyevent(json):
    print('Received my event: ' + str(json))
    socketio.emit('my_response', json, callback=messageReceived)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/getTemp', methods=['POST'])
def getTemp():
    global pidata
    temp_data = request.json
    temp = temp_data['pi_temp']
    piname = temp_data['pi_name']
    pidata = piname+temp
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO temperature (tempdata, client) VALUES (%s, %s)", (temp, piname))
    mysql.connection.commit()
    result = cur.execute("SELECT * FROM terminals WHERE client=%s", [piname])
    if result > 0:
        data = cur.fetchone()
        user_name = data['name']
        if float(temp) > 30:
            alert_msg = user_name + "：" + temp + " 摄氏度"
            slack_payload = {"text": alert_msg}
            dingding_payload = { "msgtype": "text", "text": { "content": alert_msg } }
            try:
                slack_response = requests.post('https://hooks.slack.com/services/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', data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
                dingding_response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228', data=json.dumps(dingding_payload), headers={'Content-Type': 'application/json'})
            except requests.RequestException as e:
                print(e.message)
        if float(temp) > 33:
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
    global getclients
    def getclients():
        global display, pidata, pname
        pname = pidata[:-4]
        display = pidata[-4:]
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT name, ip, client, modem, satellite FROM terminals limit %s, %s", (startat, monitor_perpage))
        dbclients = cur.fetchall()
        global clients
        clients = []
        for dc in dbclients:
            clients.append(dc['client'])
        global ips
        ips = []
        for di in dbclients:
            ips.append(di['ip'])
        global modems
        modems = []
        for dm in dbclients:
            modems.append(dm['modem'])
        global satellites
        satellites = []
        for ds in dbclients:
            satellites.append(ds['satellite'])
        global ccount
        ccount = len(clients)
        global names
        names = []
        for dn in dbclients:
            names.append(dn['name'])
        cur.close()
    getclients()
    return render_template('clientstatus.html', total_num=total_num, names=names, ips=ips, clients=clients, modems=modems, satellites=satellites, ccount=ccount, display=display, page=page, monitor_pages=monitor_pages)

@socketio.on('status')
def readvlog():
    #getclients()
    while True:
        getclients()
        with open('/home/yebin/pyprojects/myblog/vlog.log') as logfile:
            status = parse_status(logfile.read())
        newclient = status.client_list
        newclientList = []
        offlineList = []
        for cl in clients:
            if cl in newclient:
                newclientList.append(cl)
            else:
                offlineList.append(cl)
        print newclientList
        l = len(newclientList)
        socketio.emit('online', {
            'nclient': newclientList,
            'nclientlen': l,
            'tempdisplay': display,
            'pname': pname
        })
        sleep(5)


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
        newlength = len(newallclientList)
        socketio.emit('totalonline', {
            'newallclient': newallclientList,
            'newallclientlen': newlength
        })
        sleep(10)