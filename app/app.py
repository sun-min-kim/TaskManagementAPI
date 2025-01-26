from flask import Flask
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv
import os
from routes import tasks_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    app.run(debug=True)
