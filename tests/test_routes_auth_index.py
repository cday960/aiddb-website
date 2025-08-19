from unittest.mock import patch
from tests.fake_db import FakeDB


@patch("app.routes.auth_routes.get_db")
def test_index_uses_service_and_renders(mock_get_db, client, fake_encrypted_password):
    mock_get_db.return_value = FakeDB(rows=[(1, "X")], cols=["id", "name"])

    with client.session_transaction() as sess:
        sess["db_username"] = "u"
        sess["db_password"] = fake_encrypted_password

    response = client.get("/")
    assert response.status_code == 200
    assert b"id" in response.data and b"name" in response.data
    mock_get_db.assert_called_once()
