from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from models import db, Task, User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists."}), 400
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user.
    """
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Login successful."}), 200
    return jsonify({'message': 'Invalid credentials.'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logout a user.
    """
    logout_user()
    return jsonify({"message": "Logout successful."}), 200