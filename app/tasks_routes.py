from flask import Blueprint, request, jsonify
from models import db, Task
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """
    Creates a new task.
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
    Retrieve all tasks.
    """
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description,
                     'dueDate': task.due_date.isoformat(), 'status': task.status} for task in tasks])

@tasks_bp.route('/tasks/<string:id>', methods=['GET'])
@login_required
def get_task(id):
    """
    Retrieve a task by ID.
    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description,
                    'dueDate': task.due_date.isoformat(), 'status': task.status})

@tasks_bp.route('/tasks/<string:id>', methods=['PUT'])
@login_required
def update_task(id):
    """
    Update a task by ID.
    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = request.json
    task.title = data['title']
    task.description = data.get('description')
    task.due_date = datetime.fromisoformat(data['dueDate'])
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'id': task.id})

@tasks_bp.route('/tasks/<string:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    """
    Delete a task by ID.
    """
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})
