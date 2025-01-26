from flask import Blueprint, request, jsonify
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Creates a new task.
    """
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.fromisoformat(data['dueDate']),
        status=data.get('status', 'pending')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id}), 201

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks.
    """
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description,
                     'dueDate': task.due_date.isoformat(), 'status': task.status} for task in tasks])

@tasks_bp.route('/tasks/<string:id>', methods=['GET'])
def get_task(id):
    """
    Retrieve a task by ID.
    """
    task = Task.query.get_or_404(id)
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description,
                    'dueDate': task.due_date.isoformat(), 'status': task.status})

@tasks_bp.route('/tasks/<string:id>', methods=['PUT'])
def update_task(id):
    """
    Update a task by ID.
    """
    task = Task.query.get_or_404(id)
    data = request.json
    task.title = data['title']
    task.description = data.get('description')
    task.due_date = datetime.fromisoformat(data['dueDate'])
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'id': task.id})

@tasks_bp.route('/tasks/<string:id>', methods=['DELETE'])
def delete_task(id):
    """
    Delete a task by ID.
    """
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})
