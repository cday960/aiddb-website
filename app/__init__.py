from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, g
from flask_session import Session
from config import Config
from flask_wtf import CSRFProtect
from app.forms.logout_form import LogoutForm

session = Session()
csrf = CSRFProtect()

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind session and csrf tokens to the app
    session.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_forms():
        return dict(logout_form=LogoutForm())

    # Security headers (after request)
    from app.lib.security import apply_security_headers

    @app.after_request
    def _secure(response):
        return apply_security_headers(response)

    # Request-scoped DB teardown for flask.g
    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            try:
                db.close()
            except Exception:
                pass

    return app
