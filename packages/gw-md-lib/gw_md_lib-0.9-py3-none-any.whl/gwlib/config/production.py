import datetime

from . import default


class Config(default.Config):
    """
        production config
    """
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = "mysql://groundworx:groundworx@mysql/groundworx"
