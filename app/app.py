from flask import Flask
from flask_migrate import Migrate
from models import db, User
from dotenv import load_dotenv
import os
from tasks_routes import tasks_bp
from auth_routes import auth_bp
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
