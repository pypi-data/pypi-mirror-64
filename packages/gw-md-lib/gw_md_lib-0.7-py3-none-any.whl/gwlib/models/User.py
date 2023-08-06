from sqlalchemy import func

from . import db


class UserType(db.Model):
    __tablename__ = "gw_user_type"

    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)



class User(db.Model):
    __tablename__ = "gw_user"

    user_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('gw_golf_course.course_id'))
    type_id = db.Column(db.Integer, db.ForeignKey('gw_user_type.type_id'))
    name = db.Column(db.String(length=50), nullable=False)
    last = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=100), nullable=False)
    password = db.Column(db.String(length=80), nullable=False)
    phone = db.Column(db.String(length=13), nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    logo_url = db.Column(db.String(length=250))
    deleted = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())


class UserToken(db.Model):
    __tablename__ = "gw_user_token"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gw_user.user_id'))
    token = db.Column(db.String(length=40), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())