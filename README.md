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

Forms are established in `website/app/forms`, and each form will get a new file. In `login_form.py` there is a class, `LoginForm`, which extends the `FlaskForm` class. Then the attributes of the class are just whatever fields you want that form to have. Since this is a login form we need a username, password, and submit button. Username is a normal text field, so we use the `StringField`, for password we don't want the characters to be uncensored on screen so we use the `PasswordField` object, etc. All field objects are listed in great length on the [FlaskWTF docs](https://flask-wtf.readthedocs.io/en/1.2.x/#:~:text=Flask%2DWTF%20%E2%80%94%20Flask%2DWTF,Version%200.10.3).

Then those forms are imported into the routes file to be used, and passed to the `render_template` function so it can be displayed on the page. Again looking at `login.html` we use jinja templating (wrap python code in a `{{ ... }}` or `{% ... %}` block) and place `form.username.label` and `form.username` in the html file. The class parameter is just for styling using bootstrapcss.

Every single form should (I hope...) follow this structure with little deviation.

### Utility Files

Ok this one is fun. In `website/util/` there are files that are used throughout the rest of the app. The two in there right now handle all encryption/decryption logic and SQL connections.

#### `crypto_utils.py`
It decrypts and encrypts strings using the fernet key. The reason it has it's own util file is because I didn't want to type
```
password = fernet.decrypt(session["db_password"].encode()).decode()
```
every single time. Instead with this it is just `password = decrypt_string(session["db_password"])`, much nicer. Plus this isolates all encryption logic so if something with that breaks we don't have to dig through all of the route files to find the problem.

#### `custom_sql_class.py`
Handling SQL connections with pyodbc is kind of a pain, so I wrote a class that does it automatically. It defaults to `aiddb@Columbia` unless a different server and db are provided. It should automatically connect and disconnect, as well as catch query errors and throw them as a `ConnectionError` consistently instead of a bunch of different types of exceptions. Right now, and for the forseeable future, it can only run `SELECT` queries, and will yell at you for trying anything else. I don't see many use cases for modifications to the DB through an automatted process on the webapp, but that could change. It has the proper execution line in there, but it's commented out.

---

## File Structure

### app/
This houses the majority of the code. All html pages, python rendering functions, javascript code, css, and forms go here.

##### `__init__.py`
This houses the definition/ configuratino function for the Flask app. This file itself isn't responsible for starting it (`website/run.py`), but mainly for establishing which blueprints are in use.

Loading environment variables:
    - Secret key for Session storage.
    - Fernet key for encryption and decryption for session data.
These need to be sent over teams, obviously cannot host them on a repo due to security concerns.

Config object:
    - The config object is loaded from `website/config.py` and then applied. Refer to the configuration section for information on how the object works.

### Starting Dev Environment

`python run.py` runs website on http://127.0.0.1:5000/

---

## Testing Commands

### Normal Test
In /website, `pytest`

### Coverage Test
`pytest --cov=app --cov=util`
