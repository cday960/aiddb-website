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
