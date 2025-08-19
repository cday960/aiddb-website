from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
    redirect,
    session,
    url_for,
    request,
)
from app.forms.login_form import LoginForm
from app.services.db_service import list_people
from app.services.session_db import get_db
from util.custom_sql_class import SQLConnection
from util.crypto_utils import encrypt_string
from app.lib.decorators import requires_login

import os
import csv

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Try to connect using provided info
        try:
            db = SQLConnection(
                server="aiddb",
                database="Columbia",
                username=username,
                password=password,
            )
            if db.connect():
                print("Redirecting!")
                session["db_username"] = username
                session["db_password"] = encrypt_string(password)
                session.permanent = True
                return redirect(url_for("auth.index"))
            else:
                error = "Login failed. Please check credentials."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("login.html", form=form, error=error)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("db_username", None)
    session.pop("db_password", None)
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/test")
@requires_login
def test():
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

    rows, headers = db.query_with_columns(query)

    for n in rows:
        print(n)

    return render_template("test.html", results=rows, headers=headers)


@auth_bp.route("/")
@requires_login
def index():
    db = get_db()

    return render_template("index.html")


@auth_bp.route("/auditor")
@requires_login
def auditor():
    return render_template("auditor_questions.html")


@auth_bp.route("/csv/edit", methods=["GET", "POST"])
def edit_csv():
    base_dir = current_app.config.get("CSV_BASE_DIR", "./temp")
    file_path = base_dir + "/test_file.csv"

    # file_path = (
    #     request.args.get("file")
    #     if request.method == "GET"
    #     else request.form.get("file")
    # )

    csrf_enabled = current_app.config.get("WTF_CSRF_ENABLED", True)

    if not file_path:
        return render_template(
            "edit_csv.html",
            data=None,
            headers=None,
            file=None,
            csrf_enabled=csrf_enabled,
        )

    full_path = os.path.abspath(os.path.join(base_dir, file_path))

    """
    Check file path stays in base dir
    """

    """
    POST editing goes here
    """

    if request.method == "POST":
        data = []
        col = -1
        for key, value in request.form.items():
            if key.startswith("cell_"):
                _, r, c = key.split("_")
                c = int(c)
                col = max(col, c)

        row = int((len(request.form) + 1) / (col + 1)) - 1
        print(f"Cols: {col}\nRows: {row}")

        for i in range(10):
            row = []
            for j in range(20):
                row.append(request.form[f"cell_{i}_{j}"].lstrip())
            data.append(row)

    if os.path.exists(full_path):
        with open(full_path, newline="") as f:
            content = list(csv.reader(f))

        headers = content[0]
        content = content[1:]

        return render_template(
            "edit_csv.html",
            data=content,
            headers=headers,
            file=file_path,
            csrf_enabled=csrf_enabled,
        )

    flash("File not found.", "danger")
    return render_template(
        "edit_csv.html",
        data=None,
        headers=None,
        file=file_path,
        csrf_enabled=csrf_enabled,
    )
