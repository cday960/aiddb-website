from flask import Blueprint, jsonify
from app.lib.decorators import requires_login, requires_api_login
from app.services.session_db import get_db


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/version")
def version():
    return jsonify({"version": "1.0.0"})


@api_bp.route("/status")
def status():
    return jsonify({"status": "ok"})


@api_bp.route("/example")
@requires_api_login
def example():
    db = get_db()

    query = """--sql
        select top 10
            psn.personID,
            psn.studentNumber,
            idnt.lastName,
            idnt.firstName
        from
            Enrollment as enrl
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
            and psn.studentNumber is not null;
    """

    rows, cols = db.query_with_columns(query)

    data = []

    for n in rows:
        data.append(dict(zip(cols, n)))

    print(data)

    return jsonify({"data": data})
