from flask import Blueprint, request, jsonify
from models import db, Task
from datetime import datetime
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """
    Create a new task for logged-in user.

    Accepts a JSON containing the following:
    - `title` (string): The title of the task.
    - `description` (string): A description of the task.
    - `dueDate` (string): The due date of the task in ISO 8601 format (e.g., "2025-01-01T12:00:00").
    - `status` (string): The status of the task. Either "pending", "in-progress", or "completed".

    Possible Responses:
    - 201: Task created successfully, returns the task ID.
    """
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.fromisoformat(data['dueDate']),
        status=data.get('status', 'pending'),
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id}), 201

@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """
    Retrieve all tasks for logged-in user.

    Doesn't require a JSON. Retrieves all tasks associated with `current_user.id`.

    Possible Responses:
    - 200: Returns a list of tasks in the following format:
        [{ "id": <task_id>, "title": <task_title>, "description": <task_description>, 
        "dueDate": <due_date_in_ISO_format>, "status": <task_status> }, ...]
    - 404: No tasks found for the logged-in user.
    """
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    if not tasks:
        return jsonify({"message": "No tasks found for the current user."}), 404
    else:
        return jsonify([{'id': task.id, 'title': task.title, 'description': task.description,
                         'dueDate': task.due_date.isoformat(), 'status': task.status} for task in tasks]), 200

@tasks_bp.route('/tasks/<string:id>', methods=['GET'])
@login_required
def get_task(id):
    """
    Retrieve a task by ID for logged-in user.

    Path Parameter:
    - `id` (string): The ID of the task to retrieve.

    Doesn't reqyure a JSON. Fetches task with given `id` if it belongs to the logged-in user.

    Possible Responses:
    - 200: Returns the task in the following format:
    {"id": <task_id>, "title": <task_title>, "description": <task_description>, 
    "dueDate": <due_date_in_ISO_format>, "status": <task_status>}
    - 404: Task not found or does not belong to the logged-in user.
    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": f"No task found with ID {id} for the current user."}), 404
    else:
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description,
                        'dueDate': task.due_date.isoformat(), 'status': task.status}), 200

@tasks_bp.route('/tasks/<string:id>', methods=['PUT'])
@login_required
def update_task(id):
    """
    Update a task by ID for logged-in user only if it belongs to the logged-in user.

    Path Parameter:
    - `id` (string): The ID of the task to update .

    Accepts a JSON containing the following:
    - `title` (string): The updated title of the task.
    - `description` (string): The updated description of the task.
    - `dueDate` (string): The updated due date in ISO 8601 format (e.g., "2025-01-01T12:00:00").
    - `status` (string): The updated status of the task. Either "pending", "in-progress", or "completed".

    Possible Responses:
    - 200: Task updated successfully, returns the task ID.
    - 400: Missing or invalid fields in JSON, or update operation failed.
    - 404: Task not found or does not belong to the logged-in user.
    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": f"No task found with ID {id} for the current user."}), 404
    
    data = request.json
    try:
        task.title = data['title']
        task.description = data.get('description')
        task.due_date = datetime.fromisoformat(data['dueDate'])
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify({'id': task.id}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update task.", "error": str(e)}), 400

@tasks_bp.route('/tasks/<string:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    """
    Delete a task by ID for logged-in user only if it belongs to the logged-in user.

    Path Parameter:
    - `id` (string): The ID of the task to delete.

    Doesn't reqyure a JSON. Fetches task with given `id` if it belongs to the logged-in user.

    Possible Responses:
    - 200: Task deleted successfully, returns a confirmation message.
    - 404: Task not found or does not belong to the logged-in user.
    - 400: Deletion operation failed.

    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": f"No task found with ID {id} for the current user."}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True, 'message': f'Task {id} deleted successfully.'}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete task.", "error": str(e)}), 400
