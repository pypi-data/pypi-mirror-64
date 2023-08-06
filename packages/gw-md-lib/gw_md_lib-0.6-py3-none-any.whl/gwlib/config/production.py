import datetime

from .default import Config


class Config(Config):
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = "mysql://groundworx:groundworx@mysql/groundworx"