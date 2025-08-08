from functools import wraps
from flask import session, redirect, url_for, flash
from cryptography.fernet import InvalidToken
from util.crypto_utils import decrypt_string

def requires_login(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        username = session.get("db_username")
        enc_pass = session.get("db_password")

        if not username or not enc_pass:
            flash("Please log in.", "warning")
            return redirect(url_for("auth.login"))
        
        try:
            # Validate password is valid
            decrypt_string(enc_pass)
        except InvalidToken:
            session.clear()
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for("auth.login"))

        return fn(*args, **kwargs)
    return _wrap
