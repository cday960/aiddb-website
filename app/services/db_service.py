from typing import List, Dict, Tuple, Any

import pyodbc

from app.dao.mssql_dao import get_top_people
from app.services.session_db import get_db


def list_people(limit: int = 10) -> Tuple[List[pyodbc.Row], List[str]]:
    db = get_db()
    rows, cols = get_top_people(db, limit=limit)
    return rows, cols
