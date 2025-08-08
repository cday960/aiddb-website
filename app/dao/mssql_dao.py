from typing import Any, Iterable, Tuple, List, Dict

from util.custom_sql_class import SQLUtilities


def rows_to_dicts(
    rows: Iterable[Tuple[Any, ...]], cols: List[str]
) -> List[Dict[str, Any]]:
    return [dict(zip(cols, r)) for r in rows]


def select_with_columns(db, query: str, params: tuple | None = None):
    return db.query_with_columns(query, params)


def get_top_people(db, limit: int = 10):
    limit = int(limit) if limit and int(limit) > 0 else 10

    sql = f"""--sql
    select top {limit}
        psn.personID,
        psn.studentNumber,
        idnt.lastName,
        idnt.firstName,
    from Enrollment as enrl
    join Calendar as cal
        on cal.calendarID = enrl.calendarID
        and cal.endYear = 2026
        and cal.summerSchool = 0
    join Person as psn
        on enrl.personID = psn.personID
        and psn.stateID is null
    join [Identity] as idnt
        on psn.currentIdentityID = idnt.identityID
    where enrl.serviceType = 'P'
    order by psn.personID;
    """

    return db.query_with_columns(sql)
