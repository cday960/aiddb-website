import time
from flask import Blueprint, render_template, redirect, session, url_for
from app.forms.login_form import LoginForm
from util.custom_sql_class import SQLConnection, SQLUtilities
from util.crypto_utils import encrypt_string, decrypt_string

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
            db = SQLUtilities(
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


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/")
def index():
    if "db_username" not in session or "db_password" not in session:
        return redirect(url_for("auth.login"))

    db = SQLUtilities(
        server="aiddb",
        database="Columbia",
        username=session["db_username"],
        password=decrypt_string(session["db_password"]),
    )

    with db:
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

        start_time = time.time()

        result = db.query(query)

        for n in result:
            print(n)

        end_time = time.time()
        query_running_time = end_time - start_time

        headers = ["Person ID", "Student Number", "Last Name", "First Name"]

    return render_template(
        "new.html", results=result, headers=headers, time=query_running_time
    )
