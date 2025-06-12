import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', f"sqlite:///{os.path.join(basedir, '..', 'dev.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class ProdConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class TestingConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'test-secret')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = False


config_by_name = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestingConfig
}
