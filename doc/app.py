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
import hashlib
import cgi

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevelopmentConfig')
app.config.from_pyfile('config.py')

global perpage
perpage = 5
# init MYSQL
mysql = MySQL(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            # flash('Unauthorized, Please login.', 'danger')
            # flash("未授权，请先登录。", 'danger')
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

# Check if user is wxtx
def is_wxtx(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'wxtx':
            return f(*args, **kwargs)
        else:
            # flash("操作未授权！", 'danger')
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
	
# Article Form Class
class ArticleForm(Form):
    title = StringField("标题", [validators.Length(min=1, max=200)])
    owner = StringField("所属者", [validators.Length(min=1, max=100)])
    body = TextAreaField("内容", [validators.Length(min=1)])

# Search Form Class
class SearchForm(Form):
    keyword = StringField("文档搜索", [validators.Length(min=1, max=50)])

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
	
# Index
@app.route('/')
@app.route('/index')
@is_wxtx
def index():
    return render_template('home.html')

# mp
@app.route('/mp')
def mp():
    return redirect(url_for('static',filename='MP_verify_2yJF2WWPOOiHbCpo.txt'))

# weixin
@app.route('/wx',methods=['GET','POST'])
def wx():
    if request.method == 'GET':
        my_signature = request.args.get('signature')
        my_timestamp = request.args.get('timestamp')
        my_nonce = request.args.get('nonce')
        my_echostr = request.args.get('echostr')

        token = 'yebin1982'

        data = [token,my_timestamp,my_nonce]
        data.sort()

        temp = ''.join(data)

        mysignature = hashlib.sha1(temp).hexdigest()

        if my_signature == mysignature:
            return my_echostr

# public 
@app.route('/public', defaults={'page':1})
@app.route('/public/<int:page>')
@is_logged_in
def public(page):
    cur = mysql.connection.cursor()
    public_owner = 'public'
    result = cur.execute("SELECT * FROM articles WHERE owner=%s ORDER BY id DESC", [public_owner])
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles WHERE owner=%s ORDER BY id DESC limit %s, %s", ([public_owner], startat, perpage))
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/public.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('links/public.html', msg=msg, page=page, pages=pages)
    cur.close()

'''
# shanghaixiaofang 
@app.route('/shfd')
@is_logged_in
def shfd():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/shfd.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/shfd.html', msg=msg)
    cur.close()

# hubeiwuwei 
@app.route('/hbrmc')
@is_logged_in
def hbrmc():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/hbrmc.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/hbrmc.html', msg=msg)
    cur.close()

# shanghaiwuwei 
@app.route('/shrmc')
@is_logged_in
def shrmc():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/shrmc.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/shrmc.html', msg=msg)
    cur.close()

# shanghaizilaishui 
@app.route('/shtw')
@is_logged_in
def shtw():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/shtw.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/shtw.html', msg=msg)
    cur.close()

# fujianwuwei 
@app.route('/fjrmc')
@is_logged_in
def fjrmc():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/fjrmc.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/fjrmc.html', msg=msg)
    cur.close()

# fuzhouhuanjian 
@app.route('/fzem')
@is_logged_in
def fzem():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/fzem.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/fzem.html', msg=msg)
    cur.close()
'''

# admin documents 
@app.route('/admin')
@is_logged_in
def admin():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('links/admin.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('links/admin.html', msg=msg)
    cur.close()

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
                if session['username'] == 'wxtx':
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('user_articles'))
                flash("登录成功。", 'success')

                '''
            #    flash("登录成功。", 'success')
                if session['username'] == 'shfd':
                    return redirect(url_for('shfd'))
                elif session['username'] == 'hbrmc':
                    return redirect(url_for('hbrmc'))
                elif session['username'] == 'fzem':
                    return redirect(url_for('fzem'))
                elif session['username'] == 'shrmc':
                    return redirect(url_for('shrmc'))
                elif session['username'] == 'shtw':
                    return redirect(url_for('shtw'))
                elif session['username'] == 'fjrmc':
                    return redirect(url_for('fjrmc'))
                elif session['username'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
                '''
            else:
                error = "登录失败。"
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = "用户名不存在。"
            return render_template('login.html', error=error)
    return render_template('login.html')



# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    # flash("已注销。", 'success')
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
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM users ORDER BY id ASC limit %s, %s", (startat, perpage))
    users = cur.fetchall()
    if result > 0:
    #    return render_template('dashboard.html', articles=articles)
        return render_template('dashboard_users.html', users=users, page=page, pages=pages)
    else:
    #    msg = 'No Articles Found'
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

# Articles
@app.route('/articles', defaults={'page':1})
@app.route('/articles/<int:page>')
@is_admin
def articles(page):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg, page=page, pages=pages)
    # Close connection
    cur.close()

# User Articles
@app.route('/user_articles', defaults={'page':1})
@app.route('/user_articles/<int:page>')
#@is_admin
def user_articles(page):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles WHERE owner=%s ORDER BY id DESC", [session['username']])
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles WHERE owner=%s ORDER BY id DESC limit %s, %s", ([session['username']], startat, perpage))
    articles = cur.fetchall()
    if result > 0:
        return render_template('user_articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('user_articles.html', msg=msg, page=page, pages=pages)
    # Close connection
    cur.close()

# Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    return render_template('article.html', article=article)

# Dashboard_Articles
@app.route('/dashboard_articles',defaults={'page':1})
@app.route('/dashboard_articles/<int:page>')
#@is_logged_in
@is_admin
def dashboard_articles(page):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")
    data = cur.fetchall()
    pages = int(ceil(len(data) / float(perpage)))
    startat = (page-1)*perpage
    result = cur.execute("SELECT * FROM articles ORDER BY id DESC limit %s, %s", (startat, perpage))
    articles = cur.fetchall()
    if result > 0:
        return render_template('dashboard_articles.html', articles=articles, page=page, pages=pages)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard_articles.html', msg=msg, page=page, pages=pages)
    # Close connection
    cur.close()

def user_name(s):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username=%s", [s])
    if result > 0:
        data = cur.fetchone()
        return data['name']
	
# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
#@is_logged_in
@is_admin
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        author = user_name(session['username'])
        body = form.body.data
        owner = form.owner.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO articles(title, author, body, owner) VALUES(%s, %s, %s, %s)",(title, author, body, owner))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("新建文档完成。", 'success')
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
    form.owner.data = article['owner']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        owner = request.form['owner']
        body = request.form['body']
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE articles SET title=%s, owner=%s, body=%s WHERE id = %s", (title, owner, body, id))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash("文档更新完成。", 'success')
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
    flash("文档删除完成。", 'success')
    return redirect(url_for('dashboard_articles'))

###########################################################
# Search
# Search Form of Keyword
@app.route('/search_keyword')
@is_logged_in
def search_keyword():
    form = SearchForm(request.form)
    return render_template('search_form.html', form=form)

# Search Log By Title
@app.route('/search_article_title', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_title/<int:page>', methods=['GET','POST'])
@is_logged_in
def search_article_title(page):
    global keyword
    if session['username'] == 'admin':
        urlstr = 'search_article_title'
        #global keyword
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate():
            keyword = form.keyword.data
            keyword = '%' + keyword + '%'
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
            return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
        else:
            msg = 'No Logs Found'
            return render_template('search_result.html', msg=msg, results=results, page=page, pages=pages, urlstr=urlstr)
        cur.close()
        return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:	
        urlstr = 'search_article_title'
        #global keyword
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate():
            keyword = form.keyword.data
            keyword = '%' + keyword + '%'
            keyword = cgi.escape(keyword)
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE owner=%s AND title LIKE (%s) ORDER BY id DESC", ([session['username']], [keyword]))
        results = cur.fetchall()
        pages = int(ceil(len(results) / float(perpage)))
        startat = (page-1)*perpage
        if result_data > 0:
            cur = mysql.connection.cursor()
            result_data = cur.execute("SELECT * FROM articles WHERE owner=%s AND title LIKE (%s) ORDER BY id DESC limit %s, %s", ([session['username']], [keyword], startat, perpage))
            results = cur.fetchall()
            return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
        else:
            msg = 'No Logs Found'
            return render_template('search_result.html', msg=msg, results=results, page=page, pages=pages, urlstr=urlstr)
        cur.close()
        return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

# Search Log By Body(Content)
@app.route('/search_article_body', defaults={'page':1}, methods=['GET','POST'])
@app.route('/search_article_body/<int:page>', methods=['GET','POST'])
@is_logged_in
def search_article_body(page):
    global keyword
    if session['username'] == 'admin':
        urlstr = 'search_article_body'
        #global keyword
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate():
            keyword = form.keyword.data
            keyword = '%' + keyword + '%'
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
            return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
        else:
            msg = 'No Logs Found'
            return render_template('search_result.html', msg=msg, results=results, page=page, pages=pages, urlstr=urlstr)
        cur.close()
        return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
    else:	
        urlstr = 'search_article_body'
        #global keyword
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate():
            keyword = form.keyword.data
            keyword = '%' + keyword + '%'
            keyword = cgi.escape(keyword)
        cur = mysql.connection.cursor()
        result_data = cur.execute("SELECT * FROM articles WHERE owner=%s AND body LIKE (%s) ORDER BY id DESC", ([session['username']], [keyword]))
        results = cur.fetchall()
        pages = int(ceil(len(results) / float(perpage)))
        startat = (page-1)*perpage
        if result_data > 0:
            cur = mysql.connection.cursor()
            result_data = cur.execute("SELECT * FROM articles WHERE owner=%s AND body LIKE (%s) ORDER BY id DESC limit %s, %s", ([session['username']], [keyword], startat, perpage))
            results = cur.fetchall()
            return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)
        else:
            msg = 'No Logs Found'
            return render_template('search_result.html', msg=msg, results=results, page=page, pages=pages, urlstr=urlstr)
        cur.close()
        return render_template('search_result.html', results=results, page=page, pages=pages, urlstr=urlstr)

if __name__ == '__main__':
    #app.run('0.0.0.0', 443, ssl_context=('fullchain1.pem', 'privkey1.pem'))
    app.run('0.0.0.0', 8021)
