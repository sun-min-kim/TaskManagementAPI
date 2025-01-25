from flask import Flask
from .routes import setup_routes

def create_app():
    app = Flask(__name__)

    with app.app_context():
        setup_routes(app)

    return app

