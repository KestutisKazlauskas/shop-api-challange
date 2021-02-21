import os


class MainConfig:
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')


class DevelopmentConfig(MainConfig):
    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db/{os.getenv('DB')}"


class TestingConfig(MainConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}