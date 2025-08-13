from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, g
from flask_session import Session
from flask_session.base import secrets
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

    # --- NONCE ---
    """
    Before any view function is called (before_request), a nonce
    token is set in the headers to allow inline js in HTML files
    while still keeping them safe from injected scripts.

    NOTE: If a response object is returned from any function decorated
    with before_request, then the view function will not be called and
    that returned response object is immediately sent to the user.
    """

    @app.before_request
    def _set_csp_nonce():
        g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def inject_csp_nonce():
        return {"csp_nonce": getattr(g, "csp_nonce", "")}

    # Security headers (after request)
    """
    After the view function is called (after_request), we set security
    headers on the response object before it is sent to the user.
    """
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
