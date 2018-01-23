class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SECRET_KEY = '\xddL\x84P<\x17\xff\x93\xcc\xb3\x88\x1d\xe8\xa7D\xe5J\xb39\x8d9\xf2\xfcV'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '840821'
    MYSQL_DB = 'log'
    MYSQL_CURSORCLASS = 'DictCursor'

class TestingConfig(Config):
    TESTING = True
