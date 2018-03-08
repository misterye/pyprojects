import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(24)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    # email server
    MAIL_SERVER = 'your.mailserver.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ['your-gmail-username@gmail.com']

class TestingConfig(Config):
    TESTING = True
