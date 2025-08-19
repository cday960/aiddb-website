from unittest.mock import patch
from app.services.db_service import list_people


@patch("app.services.db_service.get_top_people")
@patch("app.services.db_service.get_db")
def test_list_people_uses_get_db_and_dao(mock_get_db, mock_get_top_people):
    mock_get_top_people.return_value = (["row"], ["col"])
    rows, cols = list_people(limit=5)
    mock_get_db.assert_called_once()
    mock_get_top_people.assert_called_once_with(mock_get_db.return_value, limit=5)
    assert rows == ["row"] and cols == ["col"]
