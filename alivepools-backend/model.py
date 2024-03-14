# 数据库模型

from flask import Blueprint
from . import db

# Create a blueprint
bp = Blueprint("model", __name__)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    email_status = db.Column(db.Enum("verified", "unverified"), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "email_status": self.email_status,
            "created_at": self.created_at,
        }


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    send_frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.Enum("active", "deactive"), nullable=False)
    last_run_time = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("Users", backref=db.backref("tasks", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "domain": self.domain,
            "email": self.email,
            "send_frequency": self.send_frequency,
            "created_at": self.created_at,
            "status": self.status,
            "last_run_time": self.last_run_time,
        }
