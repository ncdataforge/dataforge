from flask import Flask
from .routes import main

def create_app() -> Flask:
    app = Flask(__name__)

    # Specify config environment
    app.config.from_pyfile('config.py')

    # Flask blueprint
    app.register_blueprint(main)

    return app