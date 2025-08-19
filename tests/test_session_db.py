from unittest.mock import patch
from cryptography.fernet import InvalidToken
from flask import g, session
import pytest

from app.services.session_db import get_db


def test_get_db_no_session_raises(app):
    with app.test_request_context("/"):
        with pytest.raises(RuntimeError, match="Not Authenticated"):
            get_db()


@patch("app.services.session_db.decrypt_string", side_effect=InvalidToken)
def test_get_db_invalid_token(mock_decrypt, app):
    with app.test_request_context("/"):
        session["db_username"] = "u"
        session["db_password"] = "bad"
        with pytest.raises(RuntimeError, match="Invalid session token"):
            get_db()


@patch("app.services.session_db.SQLConnection")
@patch("app.services.session_db.decrypt_string", return_value="pw")
def test_get_db_returns_connection(mock_decrypt, mock_sql_conn, app):
    with app.test_request_context("/"):
        session["db_username"] = "u"
        session["db_password"] = "token"
        instance = mock_sql_conn.return_value
        instance.connect.return_value = True
        db = get_db()
        assert db is instance
        instance.connect.assert_called_once()
        assert g.db is instance
