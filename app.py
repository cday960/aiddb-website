import pyodbc
import time
from flask import Flask, render_template, request, redirect, session, url_for
from util.custom_sql_class import SQLConnection, SQLUtilities
from typing import List


app = Flask(__name__)
app.secret_key = "test_secret_key"


@app.route("/")
def index():
    if "db_username" not in session or "db_password" not in session:
        return redirect(url_for("login"))

    db = SQLUtilities(server="aiddb", database="Columbia")
    print("Username: ", session["db_username"])
    db.username = session["db_username"]
    db.password = session["db_password"]

    with db:
        query = """--sql
            select top 10
                psn.personID,
                psn.stateID,
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

        end_time = time.time()
        query_running_time = end_time - start_time

        # for n in result:
        #     print(n)

        headers = ["Person ID", "State ID", "Student Number", "Last Name", "First Name"]

    # return render_template("index.html", results=result, headers=headers)
    return render_template(
        "new.html", results=result, headers=headers, time=query_running_time
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # print("Username: ", username, " | Password: ", password)

        # Try to connecto using provided info
        try:
            db = SQLConnection(server="aiddb", database="Columbia")
            db.username = username
            db.password = password
            # with SQLUtilities(
            #     server="aiddb",
            #     database="Columbia",
            #     username=username,
            #     password=password,
            # ) as db:
            if db.connect():
                print("Redirecting!")
                session["db_username"] = username
                session["db_password"] = password
                return redirect(url_for("index"))
            else:
                error = "Login failed. Please check credentials."
        except Exception as e:
            error = f"Error: {str(e)}"
    return render_template("login.html", error=error)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
