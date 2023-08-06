from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from . import GolfCourse, User, Hole, Alert, Sensor, Report