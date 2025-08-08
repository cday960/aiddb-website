from unittest.mock import patch, MagicMock
from util.custom_sql_class import SQLConnection


class FakeDB:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def query_with_columns(self, query, params=None, strip=False):
        return ([(1, "X")], ["id", "name"])


@patch("app.routes.auth_routes.get_db", return_value=FakeDB())
def test_index_uses_service_and_renders(mock_get_db, client, fake_encrypted_password):
    with client.session_transaction() as sess:
        sess["db_username"] = "u"
        sess["db_password"] = fake_encrypted_password

    response = client.get("/")
    assert response.status_code == 200
    assert b"id" in response.data and b"name" in response.data
    mock_get_db.assert_called_once()
