"""
Return the app after creating our function
"""

from flask import Flask, jsonify, Blueprint
from app.api.v1.admin.routes import path_1 as meetups
from app.api.v1.questions.routes import path_1 as questions
from app.api.v1.users.routes import path_1 as users

from config import app_config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(meetups)
    app.register_blueprint(questions)
    app.register_blueprint(users)

    return app