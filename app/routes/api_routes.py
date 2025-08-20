from flask import Blueprint, jsonify
from app.lib.decorators import requires_login
from app.services.session_db import get_db


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/version")
def version():
    return jsonify({"version": "1.0.0"})


@api_bp.route("/status")
def status():
    return jsonify({"status": "ok"})


@requires_login
@api_bp.route("/example")
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

    result = db.query(query)

    return jsonify({"result": result})
