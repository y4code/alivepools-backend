from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://doadmin:AVNS_XZO6vDqdYsFGGBA2G8W@db-mysql-sgp1-19924-do-user-15764718-0.c.db.ondigitalocean.com:25060/defaultdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    user = db.relationship('Users', backref=db.backref('tasks', lazy=True))

# Create a user
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user = Users(email=data['email'], email_status=data['email_status'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

#Query all users
@app.route('/query_users', methods=['GET'])
def query_users():
    users = Users.query.all()
    users_list = []
    for user in users:
        users_list.append({'email': user.email, 'email_status': user.email_status})
    return jsonify({'users': users_list}), 200

# Query a user by id
@app.route('/query_user_by_id/<int:id>', methods=['GET'])
def query_user_by_id(id):
    user = Users.query.get_or_404(id)
    return jsonify({'email': user.email, 'email_status': user.email_status}), 200

# Query a user by email
@app.route('/query_user_by_email/<string:email>', methods=['GET'])
def query_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({'email': user.email, 'email_status': user.email_status}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Delete a user
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Create a task
@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    task = Tasks(user_id=data['user_id'], domain=data['domain'], email=data['email'], send_frequency=data['send_frequency'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

# Delete a task
@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200