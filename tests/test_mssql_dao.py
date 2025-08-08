from app.dao.mssql_dao import rows_to_dicts, select_with_columns, get_top_people


class FakeDB:
    def __init__(self, rows, cols):
        self._rows, self._cols = rows, cols

    def query_with_columns(self, query, params=None):
        return self._rows, self._cols


def test_rows_to_dicts():
    rows = [(1, "A"), (2, "B")]
    cols = ["id", "name"]
    assert rows_to_dicts(rows, cols) == [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]


def test_select_with_columns():
    db = FakeDB(rows=[(1,)], cols=["x"])
    rows, cols = select_with_columns(db, "SELECT 1")
    assert rows == [(1,)]
    assert cols == ["x"]
