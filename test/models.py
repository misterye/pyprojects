from app import app
from app import db

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

#class Base(db.Model):
#    __abstract__ = True

class Test1(db.Model):
    __tablename__ = 'test1'
    __searchable__ = ['name','address','email','telephone']

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime(), nullable=False)

    #def __repr__(self):
    #    return '<Test1 %r>' % (self.address)

if enable_search:
    whooshalchemy.whoosh_index(app, Test1)