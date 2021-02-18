import os


class MainConfig:
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')
    REST_URL_PREFIX = '/api'


class DevelopmentConfig(MainConfig):
    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True


class TestingConfig(MainConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}