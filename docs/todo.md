---
title: unorganized info
nav_order: 4
---

This is all documentation that was in the readme that I haven't organized into the wiki yet.

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
