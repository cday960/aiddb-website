from unittest.mock import patch
from flask import g
from tests.fake_db import FakeDB


def test_api_example_requires_auth(client):
    response = client.get("/api/example")
    assert response.status_code == 401
    assert response.get_json()["error"]


def test_api_example_invalid_credentials(client):
    response = client.get(
        "/api/example",
        headers={"db_username": "u", "db_password": "bad"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"]


# @patch("app.lib.decorators.SQLConnection")
# @patch("app.routes.api_routes.get_db")
@patch("app.lib.decorators.get_db")
def test_api_example_valid_credentials(mock_get_db, client):
    db = FakeDB

    def fake_get_db():
        g.db = db
        return db

    mock_get_db.side_effect = fake_get_db

    response = client.get(
        "/api/example",
        headers={"db_username": "u", "db_password": "secret"},
    )

    assert response.status_code == 200
    # assert response.get_json() == {"data": [["1", "2", "3"], ["a", "b", "c"]]}
