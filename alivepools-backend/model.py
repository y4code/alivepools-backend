from flask import Blueprint
from . import db

# Create a blueprint
bp = Blueprint('model', __name__)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    email_status = db.Column(db.Enum('verified', 'unverified'), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    send_frequency = db.Column(db.String(50), nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('Users', backref=db.backref('tasks', lazy=True))
