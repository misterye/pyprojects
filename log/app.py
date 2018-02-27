# coding=utf-8
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify, send_from_directory
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from math import ceil
import hashlib
import cgi
import json
from collections import OrderedDict

#import ast

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')
global perpage
perpage = 10

#app.debug = True
# init MYSQL
mysql = MySQL(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("未授权，请先登录。", 'danger')
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
	
# Log Form Class
class LogForm(Form):
    title = StringField("标题")
    body = TextAreaField("内容", [validators.Length(min=1)])

# Search Form Class
class SearchForm(Form):
    keyword = StringField("日志查询", [validators.Length(min=1, max=50)])

class AddForm(Form):
    content = StringField('', [validators.Length(min=1, max=255)])

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
        flash("注册成功，请登录。", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Index
@app.route('/')
@app.route('/index')
def index():
    #return render_template('home.html')
    return redirect(url_for('user_logs'))

# User login
#@app.route('/', methods=['GET', 'POST'])
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
                return redirect(url_for('user_logs'))
            else:
                error = "登录失败。"
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = "用户名不存在。"
            return render_template('login.html', error=error)
    return render_template('login.html')

# user logs 
@app.route('/user_logs', defaults={'page':1})
@app.route('/user_logs/<int:page>')
@is_logged_in
def user_logs(page):
    cur = mysql.connection.cursor()
    #result = cur.execute("SELECT * FROM logs")
    result = cur.execute("SELECT * FROM logs WHERE author=%s ORDER BY id DESC", [session['username']])
    data = cur.fetchall()
    #perpage = 3
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    cur = mysql.connection.cursor()
    #result = cur.execute("SELECT * FROM logs ORDER BY id DESC limit %s, %s", (startat, perpage))
    result = cur.execute("SELECT * FROM logs WHERE author=%s ORDER BY id DESC limit %s, %s", ([session['username']], startat, perpage))
    logs = cur.fetchall()
    if result > 0:
        return render_template('user_logs.html', logs=logs, page=page, pages=pages)
    else:
        msg = 'No Logs Found'
        return render_template('user_logs.html', msg=msg, page=page, pages=pages)
    cur.close()


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))
	
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
    #perpage = 3
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM users ORDER BY id ASC limit %s, %s", (startat, perpage))
    users = cur.fetchall()
    if result > 0:
        return render_template('dashboard_users.html', users=users, page=page, pages=pages)
    else:
        msg = 'No User Found'
        return render_template('dashboard_users.html', msg=msg, page=page, pages=pages)
    # Close connection
    cur.close()
	
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

# Logs
@app.route('/logs', defaults={'page':1})
@app.route('/logs/<int:page>')
@is_admin
def logs(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get logs
    result = cur.execute("SELECT * FROM logs ORDER BY id DESC")
    data = cur.fetchall()
    #perpage = 3
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM logs ORDER BY id DESC limit %s, %s", (startat, perpage))
    logs = cur.fetchall()
    if result > 0:
        return render_template('logs.html', logs=logs, page=page, pages=pages)
    else:
        msg = 'No Logs Found'
        return render_template('logs.html', msg=msg, page=page, pages=pages)
    # Close connection
    cur.close()

# one user log id list 
@app.route('/log_id_list')
@is_logged_in
def log_id_list():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM logs WHERE author=%s ORDER BY id DESC", [session['username']])
    logs = cur.fetchall()
    id_list = []
    for log in logs:
        id_list.append(log['id'])
    cur.close()
    return id_list

# all user log id list 
@app.route('/all_log_id_list')
#@is_logged_in
@is_admin
def all_log_id_list():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = cur.fetchall()
    all_id_list = []
    for log in logs:
        all_id_list.append(log['id'])
    cur.close()
    return all_id_list

# Single log
@app.route('/log/<string:id>/')
@is_logged_in
def log(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get log
    result = cur.execute("SELECT * FROM logs WHERE id = %s", [id])
    log = cur.fetchone()
    user_log_id_list = log_id_list()
    list_len = len(user_log_id_list)
    return render_template('log.html', log=log, user_log_id_list=user_log_id_list, id=id, list_len=list_len)

# Single log to admin
@app.route('/log_to_admin/<string:id>/')
#@is_logged_in
@is_admin
def log_to_admin(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get log
    result = cur.execute("SELECT * FROM logs WHERE id = %s", [id])
    log = cur.fetchone()
    all_user_log_id_list = all_log_id_list()
    list_all_len = len(all_user_log_id_list)
    return render_template('log_to_admin.html', log=log, all_user_log_id_list=all_user_log_id_list, id=id, list_all_len=list_all_len)

# Dashboard_Logs
@app.route('/dashboard_logs', defaults={'page':1})
@app.route('/dashboard_logs/<int:page>')
#@is_logged_in
@is_admin
def dashboard_logs(page):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get logs
    result = cur.execute("SELECT * FROM logs ORDER BY id DESC")
    data = cur.fetchall()
    #perpage = 3
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM logs ORDER BY id DESC limit %s, %s", (startat, perpage))
    logs = cur.fetchall()
    if result > 0:
        return render_template('dashboard_logs.html', logs=logs, page=page, pages=pages)
    else:
        msg = 'No Logs Found'
        return render_template('dashboard_logs.html', msg=msg, page=pages, pages=pages)
    # Close connection
    cur.close()

# Add Log
@app.route('/add_log', methods=['GET', 'POST'])
@is_logged_in
def add_log():
    form = LogForm(request.form)
    if request.method == 'POST' and form.validate():
        author = session['username']
        title = form.title.data
        body = form.body.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO logs(title, author, body) VALUES(%s, %s, %s)",(title, author, body))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("新建日志完成。", 'success')
        return redirect(url_for('user_logs'))
    return render_template('add_log.html', form=form)

# Edit Log
@app.route('/edit_log/<string:id>', methods=['GET', 'POST'])
@is_logged_in
#@is_admin
def edit_log(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get log by id
    result = cur.execute("SELECT * FROM logs WHERE id = %s", [id])
    log = cur.fetchone()
    # Get form
    form = LogForm(request.form)
    # Populate log form fields
    form.title.data = log['title']
    form.body.data = log['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE logs SET title=%s, body=%s WHERE id = %s", (title, body, id))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("日志更新完成。", 'success')
        return redirect(url_for('user_logs'))
    return render_template('edit_log.html', form=form)

# Delete Log
@app.route('/delete_log/<string:id>', methods=['POST'])
@is_logged_in
#@is_admin
def delete_log(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM logs WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash("日志删除完成。", 'success')
    return redirect(url_for('user_logs'))

# Search Form of Keyword
@app.route('/search_keyword')
@is_logged_in
def search_keyword():
    form = SearchForm(request.form)
    return render_template('search_form.html', form=form)

# Search Log
@app.route('/search_log', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_log/<int:page>', methods=['GET','POST'])
@is_logged_in
def search_log(page):
    global keyword
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM logs WHERE author=%s AND body LIKE (%s) ORDER BY id DESC", ([session['username']], [keyword]))
    results = cur.fetchall()
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM logs WHERE author=%s AND body LIKE (%s) ORDER BY id DESC limit %s, %s", ([session['username']], [keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_result.html', results=results, page=page, pages=pages)
    else:
        msg = 'No Logs Found'
        return render_template('search_result.html', msg=msg, results=results, page=page, pages=pages)
    cur.close()
    return render_template('search_result.html', results=results, page=page, pages=pages)


# Search All Logs
@app.route('/search_all_logs', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_all_logs/<int:page>', methods=['GET','POST'])
@is_logged_in
def search_all_logs(page):
    global keyword
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        keyword = form.keyword.data
        keyword = '%' + keyword + '%'
        keyword = cgi.escape(keyword)
    cur = mysql.connection.cursor()
    result_data = cur.execute("SELECT * FROM logs WHERE body LIKE (%s) ORDER BY id DESC", [keyword])
    results = cur.fetchall()
    pages = int(ceil(len(results) / float(perpage)))
    startat = (page-1)*perpage
    if result_data > 0:
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM logs WHERE body LIKE (%s) ORDER BY id DESC limit %s, %s", ([keyword], startat, perpage))
        results = cur.fetchall()
        return render_template('search_all_result.html', results=results, page=page, pages=pages)
    else:
        msg = 'No Logs Found'
        return render_template('search_all_result.html', msg=msg, results=results, page=page, pages=pages)
    cur.close()
    return render_template('search_all_result.html', results=results, page=page, pages=pages)

# The following is a test of json post request.

@app.route('/todo', defaults={'page':1})
@app.route('/todo/<int:page>')
@is_logged_in
def todo(page):
    form = AddForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM todo WHERE user=%s AND complete IS FALSE ORDER BY id DESC", [session['username']])
    data = cur.fetchall()
    perpage = 20
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM todo WHERE user=%s AND complete IS FALSE ORDER BY id DESC limit %s, %s", ([session['username']], startat, perpage))
    incomplete = cur.fetchall()
    if result > 0:
        return render_template('todo.html', incomplete=incomplete, form=form, page=page, pages=pages)
    else:
        msg = "无未完成待办事项。"
        return render_template('todo.html', incomplete=incomplete, form=form, page=page, pages=pages)
    cur.close()

@app.route('/done', defaults={'page':1})
@app.route('/done/<int:page>')
@is_logged_in
def done(page):
    form = AddForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM todo WHERE user=%s AND complete IS TRUE ORDER BY id DESC", [session['username']])
    data = cur.fetchall()
    perpage = 20
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM todo WHERE user=%s AND complete IS TRUE ORDER BY id DESC limit %s, %s", ([session['username']], startat, perpage))
    complete = cur.fetchall()
    if result > 0:
        return render_template('done.html', complete=complete, form=form, page=page, pages=pages)
    else:
        msg = "无已完成待办事项。"
        return render_template('done.html', complete=complete, form=form, page=page, pages=pages)
    cur.close()


@app.route('/add', methods=['POST'])
@is_logged_in
def add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todo(content, user) VALUES(%s, %s)", (content, [session['username']]))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('todo'))

@app.route('/complete/<id>')
@is_logged_in
def complete(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todo SET complete=TRUE WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('todo'))

@app.route('/incomplete/<id>')
@is_logged_in
def incomplete(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todo SET complete=FALSE WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('done'))

if __name__ == '__main__':
    app.run('0.0.0.0', 8018)
