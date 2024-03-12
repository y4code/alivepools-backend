from flask import jsonify

CODE_OK = 20000
CODE_ERROR = "ERROR"
CODE_WEBSITE_NOT_AVAILABLE = "WEBSITE_NOT_AVAILABLE"
CODE_WEBSITE_NOT_FOUND = "WEBSITE_NOT_FOUND"
CODE_TASK_NOT_FOUND = "TASK_NOT_FOUND"
CODE_TASK_ALREADY_EXISTS = "TASK_ALREADY_EXISTS"
CODE_EMAIL_AND_PASSWORD_REQUIRED = "EMAIL_AND_PASSWORD_REQUIRED"
CODE_INVALID_EMAIL = "INVALID_EMAIL"
CODE_INVALID_PASSWORD = "INVALID_PASSWORD"
CODE_EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
CODE_INCORRECT_EMAIL_OR_VERIFICATION_CODE = "INCORRECT_EMAIL_OR_VERIFICATION_CODE"
CODE_INCORRECT_EMAIL_OR_PASSWORD = "INCORRECT_EMAIL_OR_PASSWORD"


def response_ok(data):
    return (
        jsonify(
            {
                "data": data,
                "is_success": True,
                "code": CODE_OK,
                "message": "",
            }
        ),
        200,
    )


def response_error(data, code, message):
    return (
        jsonify(
            {
                "data": data,
                "is_success": False,
                "code": code,
                "message": message,
            }
        ),
        200,
    )


def new_response(data, is_success, code, message, status_code):
    return (
        jsonify(
            {
                "data": data,
                "is_success": is_success,
                "code": code,
                "message": message,
            }
        ),
        status_code,
    )
