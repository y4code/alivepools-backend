# 常规用户登陆以及用户信息的逻辑? 是否和 auth.py 重复了?

from flask import request, jsonify, Blueprint
from .model import Users

# Create a blueprint
bp = Blueprint('user', __name__)

@bp.route('/login', methods=['POST'])
def login(email, password):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({'message': 'Login successful', 'user': {'email': user.email, 'email_status': user.email_status}}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401