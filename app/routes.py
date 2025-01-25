# app/routes.py
from flask import Blueprint, jsonify, request

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Creates a new task.

    Example `curl` command to test this route:
    curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{
    }'
    """
    data = request.json
    return jsonify({'update': 'create_task request received'})

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks.

    Example `curl` command to test this route:
    curl http://localhost:5000/tasks
    """
    return jsonify({'update': 'get_tasks request received'})

@tasks_bp.route('/tasks/<uuid:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retrieve a task by ID.
    """
    return jsonify({'update': 'get_task(id) request received'})

@tasks_bp.route('/tasks/<uuid:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a task by ID.
    """
    return jsonify({'update': 'update_task(id) request received'})

@tasks_bp.route('/tasks/<uuid:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    return jsonify({'update': 'delete_task(id) request received'})

def setup_routes(app):
    """
    Registers all blueprints for the Flask application.
    """
    app.register_blueprint(tasks_bp)
