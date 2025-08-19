class FakeDB:
    """
    Mock db for :class: SQLConnection in tests

    :param rows: list | tuple | None
        Sequence of rows to return for all queries.
    :param cols: list | tuple | None
        Column names returned by :method: query_with_columns
    """

    def __init__(self, rows=None, cols=None):
        self.rows = rows or []
        self.cols = cols or []
        self.queries = []

    def query(self, query, params=None):
        """
        Return present rows and record query
        """
        if query.lstrip().startswith("--sql"):
            query = query[5:]
        self.queries.append((query, params))
        return self.rows

    def query_with_columns(self, query, params=None):
        """
        Return present rows and cols, record query
        """
        if query.lstrip().startswith("--sql"):
            query = query[5:]
        self.queries.append((query, params))
        return self.rows, self.cols
