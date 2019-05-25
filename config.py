import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    ADMIN_FULLNAMES = os.environ.get('ADMIN_FULLNAMES') or 'Administrator'
    ADMIN_PHONE_NUMBER = os.environ.get('ADMIN_PHONE_NUMBER') or '0712345678'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'P@ssw0rd!'

    DEBUG = False
    FLASK_DEBUG = 0

class DevelopmentConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True



class TestConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    CSRF_ENABLED = False
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
  
configs = dict(
    testing = TestConfig,
    production=Config,
    development=DevelopmentConfig
)