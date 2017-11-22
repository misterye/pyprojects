import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:840821@localhost/test'
    #WHOOSH_BASE = os.path.join(basedir, 'search.db')
    #MAX_SEARCH_RESULTS = 50
    #SQLALCHEMY_TRACK_MODIFICATIONS = True
    #MSEARCH_INDEX_NAME = 'whoosh_index'
    # simple,whoosh
    #MSEARCH_BACKEND = 'whoosh'
    # auto create or update index
    #MSEARCH_ENABLE = True
    #MYSQL_HOST = 'localhost'
    #MYSQL_USER = 'root'
    #MYSQL_PASSWORD = '840821'
    #MYSQL_DB = 'test'
    #MYSQL_CURSORCLASS = 'DictCursor'

class TestingConfig(Config):
    TESTING = True
