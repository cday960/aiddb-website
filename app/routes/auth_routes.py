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


def run_missing_grade_level_tool(df):
    identifiers = [
        "LastName",
        "FirstName",
        "LocCourseNum",
        "LocCourseName",
    ]

    occur, users = create_mask("CourseGradeLevel", df, identifiers)

    export_df = create_export_df(occur, identifiers)
    return export_df


def run_missing_edssn(df):
    identifiers = ["LastName", "FirstName"]
    occur, users = create_mask("EDSSN", df, identifiers)
    users_list_no_dupes = users.drop_duplicates().values.tolist()

    db = get_db()

    pairs_sql = ", ".join(["(?, ?)"] * len(users_list_no_dupes))
    sql = f"""--sql
    select p.staffNumber, i.lastName, i.firstName
    from [Person] as p
    join [Identity] as i
        on i.identityID = p.currentIdentityID
    join (values {pairs_sql}) as v(lastName, firstName)
        on i.firstName = v.firstName
        and i.lastName = v.lastName
    where p.staffNumber is not null;
    """
    params = [x for fn, ln in users_list_no_dupes for x in (fn, ln)]
    result = db.query(sql, params)

    final = {}
    for n in result:
        name = (n[1], n[2])
        if n[0][0].lower() == "s":
            edssn = n[0]
        else:
            edssn = "000" + n[0][1:]
        final[name] = [edssn, occur[name]]

    export_list = []
    for key, value in final.items():
        export_list.append(
            [
                key[0],
                key[1],
                f"{key[0]}, {key[1]}",
                value[0],
                ", ".join(str(item) for item in value[1]),
            ]
        )

    headers = ["LastName", "FirstName", "IC Name", "EDSSN", "Occurences"]

    export_df = pd.DataFrame(export_list)
    export_df.columns = headers

    return export_df


COURSE_ASSIGN_TOOLS = {
    "missing_course_grade_level": {
        "label": "Missing CourseGradeLevel",
        "title": "Rows missing CourseGradeLevel",
        "empty_message": "No rows are missing CourseGradeLevel.",
        "runner": run_missing_grade_level_tool,
        "form_field": "missing_course_grade_level",
    },
    "missing_edssn": {
        "label": "Missing EDSSN",
        "title": "Rows missing EDSSN",
        "empty_message": "No rows are missing EDSSN.",
        "runner": run_missing_edssn,
        "form_field": "missing_edssn",
    },
}


def determine_tool(form):
    for key, config in COURSE_ASSIGN_TOOLS.items():
        field_name = config["form_field"]
        field = getattr(form, field_name, None)
        if field is not None and field.data:
            return key
    return None


def execute_course_assign_tool(tool_key, df):
    tool_config = COURSE_ASSIGN_TOOLS.get(tool_key)
    if not tool_config:
        raise KeyError(tool_key)

    result_df = tool_config["runner"](df)
    columns = result_df.columns.to_list()
    rows = result_df.to_dict(orient="records")

    return {
        "tool": tool_key,
        "label": tool_config["label"],
        "title": tool_config["title"],
        "columns": columns,
        "rows": rows,
        "count": len(rows),
        "empty_message": tool_config.get("empty_message"),
    }


@auth_bp.route("/course_assign", methods=["GET", "POST"])
@requires_login
def course_assign_validation():
    form = UploadForm()
    results = None

    # --- FILE UPLOAD ---
    if form.validate_on_submit():
        print("File uploaded!")
        tool_key = determine_tool(form)
        if not tool_key:
            flash("Please choose a tool to run.", "warning")
        else:
            file_storage = form.file.data
            try:
                file_storage.stream.seek(0)
                df = pd.read_csv(file_storage.stream, converters={"EDSSN": str})
                results = execute_course_assign_tool(tool_key, df)
                results["filename"] = file_storage.filename
                for key, value in results.items():
                    print(key, value)
            except KeyError as exc:
                missing_column = exc.args[0] if exc.args else "requried column"
                current_app.logger.warning(
                    "Course Assign tool '%s' missing required column: %s",
                    tool_key,
                    missing_column,
                )
                flash(
                    f"The uploaded file is missing the '{missing_column}' column required by this tool.",
                    "danger",
                )
            except Exception as exc:
                current_app.logger.exception(
                    "Failed to run Course Assign tool '%s': %s",
                    tool_key,
                    exc,
                )
                flash(
                    "Unable to process the uploaded file. Please verify that it is a valid CSV export.",
                    "danger",
                )
    elif request.method == "POST":
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, "danger")

    return render_template("course_assign_tools.html", form=form)
