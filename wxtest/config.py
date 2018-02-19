import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(24)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
