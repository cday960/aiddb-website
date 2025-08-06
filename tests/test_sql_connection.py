from util.custom_sql_class import SQLConnection
from unittest.mock import patch, MagicMock
import pytest


def test_missing_credentials_raises():
    db = SQLConnection(username=None, password=None)

    with pytest.raises(ConnectionError):
        db.connect()


@patch("pyodbc.connect")
def test_successful_connect(mock_connect):
    mock_connect.return_value = MagicMock()
    db = SQLConnection(username="u", password="p")
    assert db.connect() == True
