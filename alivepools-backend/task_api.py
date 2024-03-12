from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from .database import (
    add_task,
    delete_task,
    delete_user_by_id,
    query_task_by_domain_and_userid,
    query_task_by_id_and_userid,
    query_tasks_by_user_id,
    query_user_by_id,
    update_task,
)
from .response import (
    CODE_TASK_ALREADY_EXISTS,
    CODE_TASK_NOT_FOUND,
    response_ok,
    response_error,
)  # Ensure this import is correct

bp = Blueprint("task_api", __name__)


@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_all_tasks():
    current_user_id = get_jwt_identity()
    tasks = query_tasks_by_user_id(current_user_id)
    return response_ok([task.to_dict() for task in tasks])


@bp.route("/task/<taskId>", methods=["GET"])
@jwt_required()
def get_task_by_id(taskId: str):
    current_user_id = get_jwt_identity()
    task = query_task_by_id_and_userid(taskId, current_user_id)
    if task is None:
        return response_error(None, CODE_TASK_NOT_FOUND, "Task not found")
    return response_ok(task.to_dict())


@bp.route("/task", methods=["POST"])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    task_data = request.get_json()
    task_data["email"] = query_user_by_id(current_user_id).email

    existing_task = query_task_by_domain_and_userid(
        task_data["domain"], current_user_id
    )
    if existing_task:
        return response_error(
            None, CODE_TASK_ALREADY_EXISTS, "Task with the same domain already exists"
        )

    task = add_task(
        current_user_id,
        task_data["domain"],
        task_data["email"],
        task_data["send_frequency"],
        task_data["status"],
    )
    return response_ok(task.to_dict())


@bp.route("/task/<taskId>", methods=["PUT"])
@jwt_required()
def update_task_by_id(taskId):
    current_user_id = get_jwt_identity()
    task_data = request.get_json()
    success = update_task(taskId, task_data, current_user_id)
    if success:
        return response_ok(None)
    else:
        return response_error(None, CODE_TASK_NOT_FOUND, "Task not found")


@bp.route("/task/<taskId>", methods=["DELETE"])
@jwt_required()
def delete_task_by_id(taskId):
    current_user_id = get_jwt_identity()
    if delete_task(taskId, current_user_id):
        return response_ok(None)
    else:
        return response_error(None, CODE_TASK_NOT_FOUND, "Task not found")
