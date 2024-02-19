from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, create_access_token
import random

from pymysql import IntegrityError
from .email import send_custom_email
from .database import create_user, user_exists
from .model import Users
from .otp import generate_code_by_key, verify_code, otp_storage, verification_code_prefix, email_password_pair_prefix, setStorageByKey, getStorageByKey, delByKey, check_key_in_storage
import re

bp = Blueprint('user', __name__)

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False
    return True

def validate_password(password):
    if len(password) < 8:
        return False
    return True

@bp.route('/user/signup', methods=['POST'])
def register():
    """
    required: `email`, `password`
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    if not validate_email(email):
        return jsonify({"message": "Invalid email"}), 400
    if not validate_password(password):
        return jsonify({"message": "Invalid password"}), 400

    code = generate_code_by_key(email)
    setStorageByKey(email_password_pair_prefix + email, password)
    subject = "Your verification code"
    body = f"Your verification code is {code}"
    send_custom_email(email, subject, body)
    return jsonify({"message": "Verification code sent successfully"}), 200

@bp.route('/user/signup/confirmation', methods=['POST'])
def register_confirmation():
    """
    required: `email`, `code`
    """
    data = request.get_json()
    email = data.get('email', '').strip()
    code = data.get('code', '').strip()

    if not email or not code:
        return jsonify({"message": "Email and code are required"}), 400

    if not validate_email(email):
        return jsonify({"message": "Invalid email"}), 400

    pair = email_password_pair_prefix + email

    if verify_code(email, code) and check_key_in_storage(pair):
        if user_exists(email):  # 使用user_exists函数检查用户是否存在
            return jsonify({"message": "Email already in use"}), 400
        password = getStorageByKey(pair)
        try:
            create_user(email, password)
            delByKey(pair)
            token = create_access_token(identity=email)
            return jsonify(token=token), 200
        except IntegrityError as e:
            return jsonify({"message": "An unexpected error occurred"}), 500
    else:
        return jsonify({"message": "Bad email or code"}), 400




@bp.route('/user/signin', methods=['POST'])
def login():
    """
    requied: `email`, `password`
    """
    data = request.get_json()
    email = data.get('email') or ''
    password = data.get('password') or ''
    if not validate_email(email):
        return jsonify({"message": "Invalid email"}), 400
    if not validate_password(password):
        return jsonify({"message": "Invalid password"}), 400

    user = Users.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"message": "Bad email or password"}), 401

    token = create_access_token(identity=email)
    return jsonify(token=token), 200

