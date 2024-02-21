from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

bp = Blueprint("job_api", __name__)

@bp.route("/job/<jobId>", methods=["GET"])
@jwt_required()
def get_job_by_id(jobId):
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def update_job_by_id(jobId):
    pass

def delete_job_by_id(jobId):
    pass

def get_all_jobs():
    pass

def create_new_job():
    pass
