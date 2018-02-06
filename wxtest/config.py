import os

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
