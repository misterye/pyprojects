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
from math import ceil
# escape from sql attack
import cgi

global perpage
perpage = 10

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')
mysql = MySQL(app)

# Index
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

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

@app.route('/chat', methods=['GET', 'POST'])
@is_logged_in
def chat():
    return redirect("http://satelc.com:8084/chat/chat")
    #return redirect("http://139.224.114.83:8084/chat")

@app.route('/monitor', methods=['GET', 'POST'])
@is_logged_in
def monitor():
    return redirect("http://satelc.com:8084/monitor/monitor_index")

# RSSH
@app.route('/rssh')
def rssh():
    return redirect("http://satelc.com:8085/")
    #return redirect("http://139.224.114.83:8085/")

# Articles
@app.route('/articles', defaults={'page':1})
@app.route('/articles/<int:page>')
def articles(page):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg, page=page, pages=pages)

# Single Article
@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)

@app.route('/terminals', defaults={'page':1})
@app.route('/terminals/<int:page>')
@is_logged_in
def terminals(page):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC limit %s, %s", (startat, perpage))
    terminals = cur.fetchall()
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

# Register Form Class
class RegisterForm(Form):
    name = StringField('姓名', [validators.Length(min=1, max=50)])
    username = StringField('用户名', [validators.Length(min=4, max=25)])
    usergroup = StringField('用户组', [validators.Length(min=1, max=30)])
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
    usergroup = StringField('用户组', [validators.Length(min=1, max=30)])
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
        usergroup = form.usergroup.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, username, usergroup, email, password) VALUES(%s, %s, %s, %s, %s)", (name, username, usergroup, email, password))
        mysql.connection.commit()
        cur.close()
        flash("注册成功，请登录。", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            name = data['name']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['name'] = name
                flash("登录成功。", 'success')
                return redirect(url_for('index'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
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
@is_admin
def dashboard(page):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM terminals ORDER BY id ASC limit %s, %s", (startat, perpage))
    terminals = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard.html', terminals=terminals, page=page, pages=pages)
    else:
        msg = 'No Terminal Found'
        return render_template('dashboard.html', msg=msg, page=page, pages=pages)

# Dashboard_Users
@app.route('/dashboard_users', defaults={'page':1})
@app.route('/dashboard_users/<int:page>')
@is_admin
def dashboard_users(page):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users ORDER BY id ASC")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM users ORDER BY id ASC limit %s, %s", (startat, perpage))
    users = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard_users.html', users=users, page=page, pages=pages)
    else:
        msg = 'No User Found'
        return render_template('dashboard_users.html', msg=msg, page=page, pages=pages)

# Dashboard_Articles
@app.route('/dashboard_articles', defaults={'page':1})
@app.route('/dashboard_articles/<int:page>')
@is_admin
def dashboard_articles(page):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
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
@is_admin
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash("公告发布成功。", 'success')
        return redirect(url_for('dashboard_articles'))
    return render_template('add_article.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def edit_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id = %s", (title, body, id))
        mysql.connection.commit()
        cur.close()
        flash("公告更新成功。", 'success')
        return redirect(url_for('dashboard_articles'))
    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_admin
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("公告删除成功。", 'success')
    return redirect(url_for('dashboard_articles'))

# Add Terminal - Modified
@app.route('/add_terminal', methods=['GET', 'POST'])
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO terminals(name, client, address, modem, ip, satellite, found_date, remarks) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(name, client, address, modem, ip, satellite, found_date, remarks))
        mysql.connection.commit()
        cur.close()
        flash("小站添加成功。", 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_terminal.html', form=form)

# Edit Terminal - Modified
@app.route('/edit_terminal/<string:id>', methods=['GET', 'POST'])
@is_admin
def edit_terminal(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM terminals WHERE id = %s", [id])
    terminal = cur.fetchone()
    form = TerminalForm(request.form)
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
        cur = mysql.connection.cursor()
        cur.execute("UPDATE terminals SET name=%s, client=%s, address=%s, modem=%s, ip=%s, satellite=%s,found_date=%s, remarks=%s WHERE id = %s", (name, client, address, modem, ip, satellite, found_date,remarks, id))
        mysql.connection.commit()
        cur.close()
        flash("小站更新成功。", 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_terminal.html', form=form)

# Delete Terminal - Modified 
@app.route('/delete_terminal/<string:id>', methods=['POST'])
@is_admin
def delete_terminal(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM terminals WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("小站删除成功。", 'success')
    return redirect(url_for('dashboard'))

# Edit User
@app.route('/edit_user/<string:id>', methods=['GET', 'POST'])
@is_admin
def edit_user(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE id = %s", [id])
    user = cur.fetchone()
    form = UserForm(request.form)
    form.name.data = user['name']
    form.username.data = user['username']
    form.usergroup.data = user['usergroup']
    form.email.data = user['email']
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        username = request.form['username']
        usergroup = request.form['usergroup']
        email = request.form['email']
        password = sha256_crypt.encrypt(str(request.form['newPassword']))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name=%s, username=%s, usergroup=%s, email=%s, password=%s WHERE id = %s", (name, username, usergroup, email, password, id))
        mysql.connection.commit()
        cur.close()
        flash("用户更新成功。", 'success')
        return redirect(url_for('dashboard_users'))
    return render_template('edit_user.html', form=form)

# Delete User 
@app.route('/delete_user/<string:id>', methods=['POST'])
@is_admin
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("用户删除成功。", 'success')
    return redirect(url_for('dashboard_users'))

# Messages
@app.route('/messages', methods=['GET', 'POST'])
@is_logged_in
def messages():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM messages ORDER BY create_date DESC")
    messages = cur.fetchall()
    if result > 0:
        return render_template('messages.html', messages=messages)
    else:
        msg = 'no messages found'
        return render_template('messages.html', msg=msg)
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
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM client_status")
    data = cur.fetchall()
    newperpage = 50
    pages = int(ceil(len(data) / float(newperpage)))
    startat = (page-1)*newperpage
    result = cur.execute("SELECT * FROM client_status ORDER BY id DESC limit %s, %s", (startat, newperpage))
    all_clients_status = cur.fetchall()
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
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM client_status WHERE id = %s", [id])
    client_status = cur.fetchone()
    return render_template('client_status.html', client_status=client_status)

if __name__ == '__main__':
    app.run('0.0.0.0', 8019)
