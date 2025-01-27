from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Accepts a JSON containing the following fields:
    - `username` (string): The username for the user.
    - `password` (string): The password for the user.

    Possible Responses:
    - 201: User created successfully.
    - 400: Username already exists or missing required fields.
    - 500: Unexpected server-side error.
    """
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists."}), 400

    try:
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully."}), 201
    except Exception as e:
        return jsonify({"message": "An error occurred during registration.", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate and log in a user.

    Accepts a JSON containing the following fields:
    - `username` (string): The username of the user attempting to log in.
    - `password` (string): The password for the user.

    Possible Responses:
    - 200: Login successful, user is authenticated.
    - 401: Invalid username or password.
    """
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({'message': 'Invalid credentials.'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Log out the currently authenticated user.

    Doesn't require a JSON.

    Possible Responses:
    - 200: Logout successful.
    """
    logout_user()
    return jsonify({"message": "Logout successful."}), 200