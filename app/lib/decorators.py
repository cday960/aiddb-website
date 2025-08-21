from functools import wraps
from flask import session, redirect, url_for, flash, request, g, jsonify
from cryptography.fernet import InvalidToken
from app.services.session_db import get_db
from util.crypto_utils import decrypt_string, encrypt_string
from util.custom_sql_class import SQLConnection


# MUST GO AFTER BLUEPRINT ROUTE DECORATOR!!
def requires_login(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        username = session.get("db_username")
        enc_pass = session.get("db_password")

        if not username or not enc_pass:
            flash("Please log in.", "warning")
            return redirect(url_for("auth.login", next=request.path))

        try:
            # Validate password is valid
            decrypt_string(enc_pass)
        except InvalidToken:
            session.clear()
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for("auth.login", next=request.path))

        return fn(*args, **kwargs)

    return _wrap


def requires_api_login(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        auth = request.authorization

        if auth and auth.username and auth.password:
            username = auth.username
            password = encrypt_string(auth.password)

        elif request.headers.get("db_username") and request.headers.get("db_password"):
            username = request.headers.get("db_username")
            password = encrypt_string(request.headers.get("db_password"))

        else:
            username = session.get("db_username")
            password = session.get("db_password")

        if not username or not password:
            return jsonify({"error": "Authentication required"}), 401

        try:
            session["db_username"] = username
            session["db_password"] = password
            get_db()
        except Exception:
            return jsonify({"error": "Invalid credentials"}), 401

        return fn(*args, **kwargs)

    return _wrap
