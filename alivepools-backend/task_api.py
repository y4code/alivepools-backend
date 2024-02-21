from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from .database import query_tasks_by_user_id

bp = Blueprint("task_api", __name__)


@bp.route("/task/<taskId>", methods=["GET"])
@jwt_required()
def get_task_by_id(taskId):
    current_user = get_jwt_identity()
    query_tasks_by_user_id()



    return jsonify(logged_in_as=current_user), 200


def update_task_by_id(taskId):
    pass


def delete_task_by_id(taskId):
    pass


def get_all_tasks():
    pass


def create_new_task():
    pass
