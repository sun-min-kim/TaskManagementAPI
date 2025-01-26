from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'in-progress', 'completed'), default='pending')

    def __repr__(self):
        return f'<Task {self.title}>'
