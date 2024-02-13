from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, create_access_token
import random
from .email import send_custom_email
from .database import create_user

otp_storage = {}

# Create a blueprint for the authentication routes
bp = Blueprint('auth', __name__)

@bp.route('/user/signin', methods=['POST'])
def signin():
    email = request.json.get('email', None)
    if not email:
        return jsonify({"message": "Email is required"}), 400

    # 生成OTP并发送邮件
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp
    # 发送邮件的逻辑（这里仅为示例，需要实现实际发送逻辑）
    subject = "Your OTP"
    body = f"Your OTP is {otp}"
    send_custom_email(email, subject, body)  # 使用自定义的发送邮件函数
    # log
    print(f"OTP for {email} is {otp}")
    return jsonify({"message": "OTP sent successfully"}), 200

@bp.route('/user/signin/confirmation', methods=['POST'])
def confirm_otp():
    email = request.json.get('email', None)
    otp = request.json.get('otp', None)

    print(f"Email: {email}, OTP: {otp}")
    
    # 验证OTP
    if email in otp_storage and otp_storage[email] == otp:

        # 验证成功后，使用 email，将 OTP 作为默认 password 创建一个新用户
        create_user(email, otp)
        
        # 清除OTP
        del otp_storage[email]
        # 创建JWT token
        token = create_access_token(identity=email)

        return jsonify(token=token), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

