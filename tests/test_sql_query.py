import pyodbc
import pytest
from unittest.mock import patch, MagicMock
from util.custom_sql_class import SQLConnection
from tests.fake_db import FakeDB


def test_query_with_columns():
    db = FakeDB(rows=[(1, "A"), (2, "B")], cols=["id", "name"])
    rows, cols = db.query_with_columns("SELECT id, name FROM X")
    assert rows == [(1, "A"), (2, "B")]
    assert cols == ["id", "name"]
    assert db.queries == [("SELECT id, name FROM X", None)]


@patch("pyodbc.connect")
def test_query_strips_sql_prefix(mock_connect):
    db = FakeDB(rows=[(1,)])
    result = db.query("--sql SELECT 1")
    assert result == [(1,)]
    executed_query, _ = db.queries[0]
    assert executed_query.strip().startswith("SELECT")


@patch("pyodbc.connect")
def test_query_without_prefix_no_strip(mock_connect):
    db = FakeDB(rows=[(1,)])
    result = db.query("SELECT 1")
    assert result == [(1,)]
    assert db.queries[0][0] == "SELECT 1"


def test_query_dicts_returns_dict_list():
    db = SQLConnection(username="u", password="p")
    db.query_with_columns = MagicMock(return_value=([(1, "A")], ["id", "name"]))
    result = db.query_dicts("SELECT id, name FROM X")
    assert result == [{"id": 1, "name": "A"}]


def test_query_without_connection_raises():
    db = SQLConnection(username="u", password="p")
    with pytest.raises(ConnectionError):
        db.query("SELECT 1")


def test_query_with_columns_without_connection_raises():
    db = SQLConnection(username="u", password="p")
    with pytest.raises(ConnectionError):
        db.query_with_columns("SELECT 1")


def test_query_non_select_returns_empty_list():
    db = SQLConnection(username="u", password="p")
    db.connection = MagicMock()
    cursor = db.connection.cursor.return_value
    cursor.execute.return_value = None
    result = db.query("UPDATE table SET col=1")
    assert result == []


def test_query_database_error_propogates():
    db = SQLConnection(username="u", password="p")
    db.connection = MagicMock()
    cursor = db.connection.cursor.return_value
    cursor.execute.side_effect = Exception("boom")
    with pytest.raises(pyodbc.DatabaseError):
        db.query("SELECT 1")
