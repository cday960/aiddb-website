# AID DB Internal Website

## Getting Started
1. Ask me to send you the `.env` file, this is necessary for encryption and app secret keys. Place env file in project directory, same folder as `run.py`.
2. In project directory, create virtual environment
```
python -m venv .venv
```
This creates your virtual environment in the folder `.venv`
3. Activate environment
Linux-
```
source .venv/bin/activate
```
Windows-
```
.\.venv\Scripts\activate.bat
```
4. Install MS C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
Make sure to install "Desktop development with C++" and "Node.js build tools".
5. Install Python packages
```
pip install -r requirements.txt
```
6. Run the server
```
python run.py
```
You can now connect to the dev site at http://127.0.0.1:5000

## Logic Structure
This app follows the blueprint factory design paradigm. Each "group" of routes, or pages, is broken up into different files. Those different files are the "blueprints" for those routes. Then the "factory", or `app/__init__.py` builds the app from the blueprints.

### Blueprints
Each blueprint serves a specific purpose and services a specific type of page. 
- `admin_routes.py` is reserved for pages that only developers should ever see such as user permissions, log information, transfer history, etc.
- `auth_routes.py` houses any pages that require authentication (not authorization), so any page that requires a username or password to be used.
- `dashboard_routes.py` is for pages that center around settings with the webapp itself such as color scheme, default export methods, query history, etc.

These blueprints are then utilized in `website/app/__init__.py`, specifically `app.register_blueprint(app.routes.auth_routes.auth_bp)`. This line is what actually "wires up" that blueprint to the app.


### Routes
Ok well how are the pages actually rendered? Inside of the routes files, there are functions with decorators above them (`@auth_bp.route("/login", methods=["GET", "POST"])`) which is responsible for sending the http file to the end user. The first argument `"/login"` is the url of that page, so the function below it (`login()`) will send that page to `/login`. The second argument is the type of request that is made. Since this is a page with a form it needs both `GET` and `POST`.

The contents of the function is responsible for sending the appropriate data with the page as it is requested. For example the login page starts off with checking for a validated form, if there isn't one (the user has not submitted their login info yet) then it returns the render function.

The render function is easy, first argument is the html file you want from `website/app/templates`. Every argument after that is data you want to use in the html file. For login that includes the login form and error if there is one. Then in `login.html` we can utilize that by displaying the error at the bottom of the page if it exists.


### Forms
Structured forms are how user input is sanitized and trusted. This webapp utilizes Flask_WTF which lets us integrate WTForms in Flask. WTForms is a simple data validation library to make sure users aren't putting js scripts into their username box, among other nefarious things.

#### Field Objects
Forms are established in `website/app/forms`, and each form will get a new file. In `login_form.py` there is a class, `LoginForm`, which extends the `FlaskForm` class. Then the attributes of the class are just whatever fields you want that form to have. 
Since this is a login form we need a username, password, and submit button. 
- Username is a normal text field, so we use the `StringField`.
- Password, we want the characters hidden on screen so we use the `PasswordField` object, etc. 
- Submit button, `SubmitField` object packages the form data into headers before resubmitting the request to the url of the page it is on. The `if` block only runs if the data is validated (the button press is what sent the request).
All field objects are listed in great length on the [FlaskWTF docs](https://flask-wtf.readthedocs.io/en/1.2.x/#:~:text=Flask%2DWTF%20%E2%80%94%20Flask%2DWTF,Version%200.10.3).

#### Validators
Validators verify that the input fits a set of criteria based off what validator object is used. The `DataRequired` object ensures the field is not empty on submit. More specifically, it checks that `form.<field>.data` exists. This is important since in the `if` block in `app/routes/auth_routes.py` we assign username and password to the form data, which wouldn't be possible if the login fields were left empty. Validators should always be used.
- [Validator Docs](https://wtforms.readthedocs.io/en/2.3.x/validators/)

#### Rendering in HTML
Then those forms are imported into the routes file to be used, and passed to the `render_template` function so it can be displayed on the page. Again looking at `login.html` we use jinja templating (wrap python code in a `{{ ... }}` or `{% ... %}` block) and place `form.username.label` and `form.username` in the html file. The class parameter is just for styling using bootstrapcss.

Every single form should (I hope...) follow this structure with little deviation.

#### Jinja
- [Official Docs](https://jinja.palletsprojects.com/en/stable/)
- [GeeksForGeeks article](https://www.geeksforgeeks.org/python/templating-with-jinja2-in-flask/)
Official docs are good for syntax, gfg article lists all info you should need to make new pages for this webapp.


---

## File Structure

### app/
This houses the majority of the code. All html pages, python rendering functions, javascript code, css, and forms go here.

#### `__init__.py`
This houses the definition/ configuratino function for the Flask app. This file itself isn't responsible for starting it (`website/run.py`), but mainly for establishing which blueprints are in use.

Loading environment variables:
    - Secret key for Session storage.
    - Fernet key for encryption and decryption for session data.
These need to be sent over teams, obviously cannot host them on a repo due to security concerns.

Config object:
    - The config object is loaded from `website/config.py` and then applied. Refer to the configuration section for information on how the object works.

#### dao/
DAO, or data access object, is where sql queries that are ran a lot will go. There are a few key properties of this folder that should be maintained to make testing and maintenance easier.
- Does not access Flask or Session
- Does not access the database directly
- Does not do any auth logic.

By keeping this folder constrained to only queries that are frequently used, if there is a problem with any query result from this file, but not other queries, then we know the problem is with this folder and the query itself, not DB connection/ auth or session management.

#### forms/
Holds the Flask-WTF forms that are used in the HTML pages. All input fields (so all forms) need to come from a python file in here.

#### lib/
This holds functions to make our lives easier. Right now it has `decorators.py` and `security.py`.

#### `decorators.py`
New function decorators are written here. Decorators are functions that establish requirements for other functions. 

Right now there is a `requires_login` decorator that when put on a route function will require that there is a valid username and password stored in the session. If there is not a valid username and password, the user is redirected to the login page. With this decorator there is no manual auth checking required, just put it above the route function!

#### `security.py`
This file contains one function that sets security headers for every response sent by the website. It is called in `app/__init__.py`, and the `@app.after_request` decorator makes the `_secure()` function a hook. 

A hook here just means that it runs everytime a certain thing happens, so in this case after a request is made to the site, and before the site sends the response object to the user, it will apply the security headers to the response object. This prevents any bad actors from being able to mess with the response object to somehow gain information or to change behavior of the website on the users end.

#### routes/
Files that compile response objects for given URLs. This is the beginning of all logic flow, so any request made to the website will look through these files first.

#### services/
This is how the database is accessed. This has two important files, `db_service.py` and `session_db.py`.

##### `db_service.py`
All of the frequently used queries from the DAO are called from here, so if you are using a DAO query in a routes file, you would import `db_service.py`, not `mssql_dao.py`. The reason this is split up is because if the DB cannot be accessed, it will error out in this file instead of the DAO file, easier to debug.

##### `session_db.py`
This is one you will use a lot because it is how you access the database. In here is the function `get_db()` which automatically pulls the user login info from the session data, builds the db object, then stores it in the global `g` object so the database can be reaccessed on the same request without having to open a new connection. 

Keeping authentication in here means that besides the initial login route, you should never have to manually get the username and password from the session data, or manually create the DB object.

### Utility Files
Ok this one is fun. In `website/util/` there are files that are used throughout the rest of the app. The two in there right now handle all encryption/decryption logic and SQL connections.

#### `crypto_utils.py`
It decrypts and encrypts strings using the fernet key. The reason it has it's own util file is because I didn't want to type
```
password = fernet.decrypt(session["db_password"].encode()).decode()
```
every single time. Instead with this it is just
```
password = decrypt_string(session["db_password"])
```
which is much nicer. Plus this isolates all encryption logic so if something with that breaks we don't have to dig through all of the route files to find the problem.

#### `custom_sql_class.py`
Handling SQL connections with pyodbc is kind of a pain, so I wrote a class that does it automatically. It defaults to `aiddb@Columbia` unless a different server and db are provided. 

It automatically connects and disconnects, as well as catches query errors and throw them as a `ConnectionError` consistently instead of a bunch of different types of exceptions.

You can manually call the connect function to test user login info, or just create the object and let it connect itself, it makes no difference.

In the future I would like to include functionality to have multiple databases in the `SQLConnection` object, so user info would be saved in the session and the list of databases is stored in the web db. Then any database the user has access to can be accessed without having to login again.

Right now, and for the forseeable future, it can only run `SELECT` queries, and will yell at you for trying anything else (it prints a warning and returns an empty list). I don't see many use cases for modifications to the DB through an automatted process on the webapp, but that could change. It has the proper execution line in there, but it's commented out.


### Starting Dev Environment

`python run.py` runs website on http://127.0.0.1:5000/

---

## Example Logic Flow
Let's take a look at the logic flow of a user opening the website at the url `localhost:5000/` for the first time (not logged in), to them being able to view the dashboard.

So the `/` route is called. First we look at `app/__init__.py` and the blueprints that are registered. The only one right now is `auth_bp` in `app.routes.auth_routes` which can be seen in the import line just above the register line.

Now in `app/routes/auth_routes.py` we go to the endpoint that was called, so `/` or the `index()` function. This function has the `@requires_login` decorator, so it jumps to that in `app/lib/decorators.py`.

Now in `app/lib/decorators.py` we see the function called by the decorator which is 
```
requires_login(fn)
```
It gets the username and password from the session data. Since the user is not logged in,
```
username = None
enc_pass = None
```
That means it fails the `if` block and the user is redirected to `auth.login`.

Since it's a redirect to an `auth` endpoint we're back in `app/routes/authoroutes.py`. We look for `login()` which is the first function. Immediately we initialize the login form object with 
```
form = LoginForm()
```
which means we need to refer to the imported class `app.forms.login_form.LoginForm`.

Once in `app/forms/login_form.py` we see it's just an object that ensures type security and data sanitization. Refer to the forms section above for more information on how this works.

Ok back in `app/routes/auth_routes.py` we hit
```
if form.validate_on_submit():
```
This will only evaluate to true if the form submit button was pressed which made the request. Since the user was redirected here by the login decorator on the index function, the `if` block evaluates to `False`, so we jump all the way down to
```
return render_template("login.html", form=form, error=error)
```
where the login page is rendered. We pass the form and error into the render command.

Ok we're on the last steps to rendering a page (yay!). In `app/templates/login.html` we see that it contains a header and a form. The form method is `POST` since the only way to access the `/login` route is with a `POST` method. This will be the case for all form requests. Then we have `username_label, username_form, password_label, password_form, submit_button`. To put the form into an HTML file it is as easy as 
```
{{ form.username.label }}
{{ form.username }}
{{ form.password.label }}
{{ form.password }}
{{ submit_button }}
```
and that's it. Everything else that is in there is for styling and organization. I split up these lines by setting the actual HTML element to a variable first, that way there is a clear separation between the code establishing how I want the form to look versus where I want it to live on the page.

Ok once the submit button is pressed it sends a POST request back to the route `/login`. Now we're back in `auth_routes.py` except this time, since the request was made by the button and is a POST request, we pass the `if` form validation block!

Now we pull the username and password out of the session data and build the db object. This is the _only place_ that the db object will be manually built instead of using `get_db()` from `session_db.py`. The reason for this is on the initial login we want to check manually that the db is connected, we're not actually utilizing it to make any queries.

We check to see if the db can connect with
```
if db.connect():
```
and if it does then we set the session data (mind how the password is encrypted with `encrypt_string(password)` __before__ it is stored into the session) and redirect the user to `auth.index`.

Alright we're on the last page. In the `index()` function in `auth_routes.py` we know the user is logged in because of the decorator so no need to check that. The user is logged into the db with `db = get_db()`, a query is initialized and then sent to the db with `db.query_with_columns(query, strip=True)` and the result is sent to the page as `results` and `headers`.

Now you don't have to use the special db methods I've built out. The `db` object will always have the method `db.query(query, strip)` which just executes a raw query and sends back the result as a list of rows and the headers will be row 0.

Then rendering `test.html` is the same as rendering `login.html`. We make a header row of `<th>` elements by looping through `headers`. Then we loop through `results` and make a new row for each element, then a new cell for each piece of data in said new row.

YAY!! That's it, the full logic flow of the website. It seems like a lot, but once you develop a couple of pages and add some new functionality, it is very easy to remember and makes intuitive sense.

## Commands

### Run server
`python app.py`

### Start Redis server
```
sudo systemctl enable --now redis-server
```

```
redis-cli ping
```
should give a response `PONG`


### Normal Test
In /website, `pytest`

### Coverage Test
`pytest --cov=app --cov=util`
