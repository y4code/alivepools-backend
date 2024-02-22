from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from .database import (
    delete_task,
    delete_user_by_id,
    query_task_by_id,
    query_tasks_by_user_id,
    update_task,
)

bp = Blueprint("task_api", __name__)


@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_all_tasks():
    print(get_jwt_identity())
    current_user_id = get_jwt_identity()
    tasks = query_tasks_by_user_id(current_user_id)
    return jsonify(tasks=[task.to_dict() for task in tasks]), 200


@bp.route("/task/<taskId>", methods=["GET"])
@jwt_required()
def get_task_by_id(taskId: str):
    current_user_id = get_jwt_identity()
    task = query_task_by_id(taskId, current_user_id)
    if task is None:
        return jsonify(error="Task not found"), 404
    return jsonify(task=task.to_dict()), 200


@bp.route("/task/<taskId>", methods=["PUT"])
@jwt_required()
def update_task_by_id(taskId):
    current_user_id = get_jwt_identity()
    task_data = request.get_json()
    success = update_task(taskId, task_data, current_user_id)
    if success:
        return jsonify(success=True), 200
    else:
        return jsonify(error="Task not found or unauthorized"), 404


@bp.route("/task/<taskId>", methods=["DELETE"])
@jwt_required()
def delete_task_by_id(taskId):
    current_user_id = get_jwt_identity()
    if delete_task(taskId, current_user_id):
        return jsonify(success=True), 204
    else:
        return jsonify(error="Task not found or unauthorized"), 404
