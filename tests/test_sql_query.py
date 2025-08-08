from unittest.mock import patch, MagicMock
from util.custom_sql_class import SQLConnection


def test_query_with_columns():
    conn = SQLConnection(
        server="aiddb", database="Columbia", username="u", password="p"
    )

    fake_cursor = MagicMock()
    fake_cursor.fetchall.return_value = [(1, "A"), (2, "B")]
    fake_cursor.description = [("id",), ("name",)]

    fake_conn = MagicMock()
    fake_conn.cursor.return_value = fake_cursor

    with patch("pyodbc.connect", return_value=fake_conn):
        conn.connect()
        rows, cols = conn.query_with_columns("SELECT id, name FROM X")
        assert rows == [(1, "A"), (2, "B")]
        assert cols == ["id", "name"]
