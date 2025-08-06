from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_session import Session
from config import Config
from flask_wtf import CSRFProtect

session = Session()
csrf = CSRFProtect()

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    session.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    return app
