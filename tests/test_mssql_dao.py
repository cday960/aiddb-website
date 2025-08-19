from app.dao.mssql_dao import rows_to_dicts, select_with_columns
from tests.fake_db import FakeDB


def test_rows_to_dicts():
    rows = [(1, "A"), (2, "B")]
    cols = ["id", "name"]
    assert rows_to_dicts(rows, cols) == [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]


def test_select_with_columns():
    db = FakeDB(rows=[(1,)], cols=["x"])
    rows, cols = select_with_columns(db, "SELECT 1")
    assert rows == [(1,)]
    assert cols == ["x"]
