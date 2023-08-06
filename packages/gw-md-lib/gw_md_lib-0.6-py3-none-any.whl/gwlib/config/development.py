import datetime

from .default import Config


class Config(Config):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql://groundworx:groundworx@mysql/groundworx"

