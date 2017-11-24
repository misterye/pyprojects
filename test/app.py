# coding=utf-8
import sys;
reload(sys);
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import hashlib
#from flask_sqlalchemy import SQLAlchemy
#import flask_whooshalchemy
#import flask.ext.sqlalchemy as flask_sqlalchemy
#from flask_whooshee import Whooshee
#import models

app = Flask(__name__)
#whooshee = Whooshee(app)
app.config.from_object('config.DevelopmentConfig')
#db = SQLAlchemy(app)

'''
@whooshee.register_model('address')
class Test1(db.Model):
    __tablename__ = 'test1'
#    __searchable__ = ['name','address','email','telephone']

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
#    email = db.Column(db.String(255), nullable=False)
#    telephone = db.Column(db.String(255), nullable=False)
#    create_time = db.Column(db.DateTime(), nullable=False)
'''

# Index
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

# Test_Users
@app.route('/test_users')
def test_users():
#    testusers = Test1.query.order_by(Test1.id).all()
    return render_template('select_action.html')
'''
# Search
@app.route("/search_results")
def search_results():
    #results = Test1.query.whoosh_search('shanghai', MAX_SEARCH_RESULTS).all()
    #results = Test1.query.whooshee_search('user1').order_by(Test1.id.desc()).all()
    results = Test1.query.whooshee_search('Shanghai').all()
    print results
    return ''
    #return render_template('search_results.html', results=results)
'''

# Get Pi Temperature
#@app.route('/gettemp', methods=['GET', 'POST'])
@app.route('/pi', methods=['POST'])
def pi():
    pi_data = request.json
    temp = pi_data['temp']
    print temp
    print jsonify(pi_data)
    return jsonify(pi_data)


if __name__ == '__main__':
    app.secret_key='fpaoiega84qddq48q0dijfe41fj0iggr9wrj'
    app.run('0.0.0.0', 8022)
