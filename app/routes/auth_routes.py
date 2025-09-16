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
from werkzeug.utils import secure_filename
from app.forms.login_form import LoginForm
from app.forms.file_upload import UploadForm, ToolForm
from app.services.db_service import list_people
from app.services.session_db import get_db
from util.custom_sql_class import SQLConnection
from util.crypto_utils import encrypt_string
from app.lib.decorators import requires_login

import os
import csv
import pandas as pd

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    next_page = request.args.get("next")
    if request.method == "GET" and next_page:
        redirect_target = next_page

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
                if next_page:
                    return redirect(next_page)
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
@requires_login
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

        col = col + 1
        row = int((len(request.form) + 1) / (col))
        print(f"Cols: {col}\nRows: {row}")

        for i in range(row):
            row = []
            for j in range(col):
                row.append(request.form[f"cell_{i}_{j}"].lstrip())
            data.append(row)

        for n in data:
            print(n)

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


def create_mask(field: str, df: pd.DataFrame, identifiers: list[str]):
    """
    Applies a mask for a dataframe given a string field/column.
    Returns a dictionary that has a first and last name key, and the
    value is a list of indexes where the given field is not present.
    """
    mask = df[field].isna() | df[field].astype(str).str.strip().eq("")

    missing_rows = df[mask]
    missing_idx = missing_rows.index

    users = missing_rows[identifiers]

    occur = {}

    for n in zip(missing_idx, users.values.tolist()):
        name = tuple([n for n in n[1]])
        if name not in occur:
            occur[name] = [n[0] + 2]
        else:
            occur[name].append(n[0] + 2)

    return (occur, users)


def create_export_df(occur, identifiers):
    export_list = []
    for key, value in occur.items():
        occ = str(value[0])
        if len(value) > 1:
            occ = ", ".join(str(item) for item in value)
        temp = [x for x in key]
        temp.append(occ)
        export_list.append(temp)

    export_df = pd.DataFrame(export_list)
    cols = identifiers
    cols.append("Occurrences")
    export_df.columns = cols

    return export_df


@auth_bp.route("/course_assign", methods=["GET", "POST"])
@requires_login
def course_assign_validation():
    # print(request.form)
    upload_form = UploadForm()
    tool_form = ToolForm()

    if request.method == "POST":
        # --- TOOLS ---
        if "tool" in request.form:
            tool_keys = request.form.keys()
            print(tool_keys)
            if "CourseGradeLevel" in tool_keys:
                print("Running operations for CourseGradeLevel validation.")
            if "EDSSN" in tool_keys:
                print("Running operations for EDSSN validation.")

        # --- FILE UPLOAD ---
        if upload_form.validate_on_submit():
            print("File uploaded!")
            file = upload_form.file.data
            filename = secure_filename(file.filename)

            df = pd.read_csv(file, converters={"EDSSN": str})

            identifiers = [
                "LastName",
                "FirstName",
                "LocCourseNum",
                "LocCourseName",
            ]

            occur, users = create_mask("CourseGradeLevel", df, identifiers)

            export_df = create_export_df(occur, identifiers)
            # print(export_df)

    tools = {
        "CourseGradeLevel": "Missing CourseGradeLevel Fields",
        "EDSSN": "Missing EDSSN Numbers",
        "DupeAssignNum": "Duplicate AssignNum Fields",
        "CourseNum": "Missing CourseNums",
        "CourseSem": "Missing CourseSems",
    }
    tool_forms = [{"key": x, "label": y, "form": ToolForm()} for x, y in tools.items()]

    return render_template(
        "course_assign_tools.html", upload_form=upload_form, tool_forms=tool_forms
    )
