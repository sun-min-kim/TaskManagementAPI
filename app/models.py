from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    User model for storing user information.
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """
        Hashes the password and stores it in the password_hash field.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifies the password against the stored hash.
        """
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    """
    Task model for storing task details.
    Each task is associated with a specific user via a foreign key.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'in-progress', 'completed'), default='pending')
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'
