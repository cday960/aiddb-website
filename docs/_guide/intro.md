---
layout: page
title: Intro
nav_order: 1
---

Basic information on the key parts of the site.

## Stack

- Flask
- Jinja2
- pyodbc
- pytest
- redis

## Architecture

This section will go over the general design and layout of the website.

### Blueprints

This app follows the blueprint factory design paradigm. Each "group" of routes, or pages, is broken up into different files. Those different files are the "blueprints" for those routes. Then the "factory", or `app/__init__.py` builds the app from the blueprints.

Each blueprint serves a specific purpose and services a specific type of page. 
- `admin_routes.py` is reserved for pages that only developers should ever see such as user permissions, log information, transfer history, etc.
- `auth_routes.py` houses any pages that require authentication (not authorization), so any page that requires a username or password to be used.
- `dashboard_routes.py` is for pages that center around settings with the webapp itself such as color scheme, default export methods, query history, etc.

These blueprints are then utilized in `website/app/__init__.py`, specifically `app.register_blueprint(app.routes.auth_routes.auth_bp)`. This line is what actually "wires up" that blueprint to the app.


### Routes

The route files contain __view functions__, or functions that return a rendered HTML file. Above each view function is a [decorator]({{ site.baseurl }}{% link _guide/decorators.md %}) that determines what route that function will serve. 

All logic required for a specific page will be in the view function. So if a page is supposed to display a table from the db, all db operations will happen within that page's view function.

The return object of a view function is what is served to the user.


### Database Access

`app/routes/auth_routes.py` -> `app/services/db_session` -> `util/custom_sql_class.py`

All database access starts with `custom_sql_class.py`. I wrote this to eliminate the overhead that comes with establishing a database connection in Python.

This file is class based so upon initializing an `SQLConnection` object, it automatically logs in, handles errors if the login fails, and automatically disconnects and frees resources once the object goes out of scope.

My goal with this is to never require hard coding any database connection information within the view functions or page logic.

---

If there are queries/ db functions that are used a lot throughout the codebase, they can be written in `app/dao/mssql_dao.py`. DAO stands for data access object, and it's a coding design where db connection, access, and utilization are spread out to be more secure, and easier to debug.

DAO code will never access the db or any flask data directly, it is only logic.

---

Now for the DAO to access the db it needs the wrapper `app/services/db_service.py`. The `services` folder contains the functions utilized by the view functions to access the db. `db_service` will contain the wrapper functions for queries in the DAO.

`db_session.py` is how the db object is initialized. It's just a wrapper to automatically check session data and do error handling.


### Templates

All html files go in the templates folder.

`base.html` is the base template that every other file builds off of using Jinja templating. This contains all of the nasty stuff we don't want to have to type into every new page, like the navbar, style and script sources, meta parameters, etc.

Read [templates](#) for more information.
