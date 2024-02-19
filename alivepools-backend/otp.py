from flask import Blueprint
import random

bp = Blueprint('otp', __name__)

# code generation and verification
def generate_code_by_key(key):
    code = str(random.randint(100000, 999999))
    setStorageByKey(key, code)
    return code

def verify_code(key, code):
    if check_key_in_storage(key) and getStorageByKey(key) == code:
        delByKey(key)
        return True
    else:
        return False

# in memory key-value storage 
otp_storage = {}
verification_code_prefix = "verification_code_"
email_password_pair_prefix = "email_password_pair_"
def setStorageByKey(key, value):
    otp_storage[key] = value
    return True

def getStorageByKey(key):
    return otp_storage[key]

def delByKey(key):
    del otp_storage[key]
    return True

def check_key_in_storage(key):
    if key in otp_storage:
        return True
    else:
        return False