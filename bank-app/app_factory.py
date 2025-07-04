# app_factory.py
from flask import Flask
from extensions import db
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from models.user_model import User
        import app_routes  # move your route definitions to app_routes.py

    return app
