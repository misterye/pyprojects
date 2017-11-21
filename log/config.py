class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '840821'
    MYSQL_DB = 'log'
    MYSQL_CURSORCLASS = 'DictCursor'

class TestingConfig(Config):
    TESTING = True
