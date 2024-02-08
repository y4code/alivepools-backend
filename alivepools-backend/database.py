from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from . import db
from .model import Users, Tasks
from datetime import datetime, timedelta
from flask import current_app

# Create a blueprint
bp = Blueprint('database', __name__)

# Create a user
@bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user = Users(email=data['email'], email_status=data['email_status'], password=data['password'], create_at=data['create_at'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

#Query all users
@bp.route('/query_users', methods=['GET'])
def query_users():
    users = Users.query.all()
    users_list = []
    for user in users:
        users_list.append({'email': user.email, 'email_status': user.email_status})
    return jsonify({'users': users_list}), 200

# Query a user by id
@bp.route('/query_user_by_id/<int:id>', methods=['GET'])
def query_user_by_id(id):
    user = Users.query.get_or_404(id)
    return jsonify({'email': user.email, 'email_status': user.email_status}), 200

# Query a user by email
@bp.route('/query_user_by_email/<string:email>', methods=['GET'])
def query_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({'email': user.email, 'email_status': user.email_status}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Delete a user
@bp.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Create a task
@bp.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    task = Tasks(user_id=data['user_id'], domain=data['domain'], email=data['email'], send_frequency=data['send_frequency'], create_at=data['create_at'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

# Query task by next_run_time <= now and status = 'active'
def query_tasks_need_to_run():
    with current_app.app_context():
        now = datetime.utcnow()
        tasks = Tasks.query.filter(
            Tasks.next_run_time <= now, 
            Tasks.status == 'active').all()
        tasks_list = []
        for task in tasks:
            tasks_list.append({'id': task.id, 'user_id': task.user_id, 'domain': task.domain, 'email': task.email, 'send_frequency': task.send_frequency, 'status': task.status, 'last_run_time': task.last_run_time, 'next_run_time': task.next_run_time})
        return jsonify({'tasks': tasks_list}), 200

# Update the last_run_time of a task
def update_last_run_time(id, last_run_time):
    task = Tasks.query.get_or_404(id)
    task.last_run_time = last_run_time
    db.session.commit()
    return jsonify({'message': 'Last run time updated successfully'}), 200

# Update the next_run_time of a task
def update_next_run_time(id, next_run_time):
    task = Tasks.query.get_or_404(id)
    task.next_run_time = next_run_time
    db.session.commit()
    return jsonify({'message': 'Next run time updated successfully'}), 200

# Delete a task
@bp.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


