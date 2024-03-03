from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, create_access_token
import random
from pymysql import IntegrityError
from .email import send_custom_email
from .database import create_user, user_exists
from .model import Users
from .otp import (
    generate_code_by_key,
    verify_code,
    otp_storage,
    verification_code_prefix,
    email_password_pair_prefix,
    setStorageByKey,
    getStorageByKey,
    delByKey,
    check_key_in_storage,
)
import re
from .response import (
    CODE_ERROR,
    CODE_EMAIL_AND_PASSWORD_REQUIRED,
    CODE_INVALID_EMAIL,
    CODE_INVALID_PASSWORD,
    CODE_EMAIL_ALREADY_EXISTS,
    CODE_INCORRECT_EMAIL_OR_VERIFICATION_CODE,
    CODE_INCORRECT_EMAIL_OR_PASSWORD,
    response_ok,
    response_error,
)


bp = Blueprint("user_api", __name__)


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False
    return True


def validate_password(password):
    if len(password) < 8:
        return False
    return True


@bp.route("/user/signup", methods=["POST"])
def register():
    """
    required: `email`, `password`
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return response_error(
            None, CODE_EMAIL_AND_PASSWORD_REQUIRED, "Email and password are required"
        )
    if not validate_email(email):
        return response_error(None, CODE_INVALID_EMAIL, "Invalid email")
    if not validate_password(password):
        return response_error(None, CODE_INVALID_PASSWORD, "Invalid password")

    code = generate_code_by_key(email)
    setStorageByKey(email_password_pair_prefix + email, password)
    subject = "Your verification code"
    body = f"Your verification code is {code}"
    send_custom_email(email, subject, body)
    return response_ok(None)


@bp.route("/user/signup/confirmation", methods=["POST"])
def register_confirmation():
    """
    required: `email`, `code`
    """
    data = request.get_json()
    email = data.get("email", "").strip()
    code = data.get("code", "").strip()

    if not email or not code:
        return response_error(
            None, CODE_EMAIL_AND_PASSWORD_REQUIRED, "Email and code are required"
        )
    if not validate_email(email):
        return response_error(None, CODE_INVALID_EMAIL, "Invalid email")

    pair = email_password_pair_prefix + email

    if verify_code(email, code) and check_key_in_storage(pair):
        if user_exists(email):
            return response_error(
                None, CODE_EMAIL_ALREADY_EXISTS, "Email already exists"
            )
        password = getStorageByKey(pair)
        try:
            user = create_user(email, password)
            delByKey(pair)
            token = create_access_token(identity=user.id)
            return response_ok({"token": token})
        except IntegrityError as e:
            return response_error(None, CODE_ERROR, "Error creating user: " + str(e))
    else:
        return response_error(
            None, CODE_INCORRECT_EMAIL_OR_VERIFICATION_CODE, "Incorrect email or code"
        )


@bp.route("/user/signin", methods=["POST"])
def login():
    """
    required: `email`, `password`
    """
    data = request.get_json()
    email = data.get("email") or ""
    password = data.get("password") or ""
    if not validate_email(email):
        return response_error(None, CODE_INVALID_EMAIL, "Invalid email")
    if not validate_password(password):
        return response_error(None, CODE_INVALID_PASSWORD, "Invalid password")

    user = Users.query.filter_by(email=email).first()
    if not user or user.password != password:
        return response_error(
            None, CODE_INCORRECT_EMAIL_OR_PASSWORD, "Incorrect email or password"
        )

    token = create_access_token(identity=user.id)
    user_data = user.to_dict()
    return response_ok({"token": token, "user": user_data})
