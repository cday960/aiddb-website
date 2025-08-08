from unittest.mock import MagicMock, patch
from util.crypto_utils import encrypt_string, decrypt_string
from util.custom_sql_class import SQLConnection

"""
TODO:
    - Write test for logout route
"""


def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_post_invalid(client):
    response = client.post(
        "/login",
        data={"username": "invalid", "password": "wrong"},
        follow_redirects=True,
    )

    assert b"Login failed" in response.data or b"Error" in response.data


def test_logout(client):
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_index_logged_out(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_require_login_redirects(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302)
    assert "/login" in response.headers["Location"]


def test_security_headers_present(client):
    response = client.get("/login")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert "default-src 'self'" in response.headers.get("Content-Security-Policy", "")


def test_requires_login_redirects_when_missing_session(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302)
    assert "/login" in response.headers["Location"]


def test_logout_post_clears_session_and_redirects(client):
    with client.session_transaction() as sess:
        sess["db_username"] = "u"
        sess["db_password"] = "token"
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code in (301, 302)
    assert "/login" in response.headers["Location"]


# @patch("app.routes.auth_routes.SQLUtilities")
# def test_index_logged_in(mock_sql_util, client, fake_encrypted_password):
#     # set session data like a user is logged in
#     with client.session_transaction() as sess:
#         sess["db_username"] = "test_user"
#         sess["db_password"] = fake_encrypted_password
#
#     # mock query result
#     mock_instance = MagicMock()
#     mock_instance.query.return_value = [("mock row",)]
#     mock_sql_util.return_value.__enter__.return_value = mock_sql_util
#
#     response = client.get("/")
#
#     assert response.status_code == 200
#     assert b"static page" in response.data
