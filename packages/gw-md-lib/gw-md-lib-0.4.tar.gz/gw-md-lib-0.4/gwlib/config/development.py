import datetime

from .base_config import Config


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql://groundworx:groundworx@mysql/groundworx"

