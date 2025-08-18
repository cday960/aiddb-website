---
layout: page
title: Routes
nav_order: 4
---

# Routes

Each file covers a different kind of page.
- `admin_routes.py`: Admin pages, such as db management page or a future page to disable server access to specific dbs, etc.
- `auth_routes.py`: Pages that require authentication, or being logged in, to access
- `dashboard_routes.py`: Pages where the __main__ logic is to display information on a page.


## Auth Routes
```python
auth_bp = Blueprint("auth", __name__)
```

This establishes a set of routes, or URLs, to be linked to the flask app.

Additional arguments allow assigning a specific templates folder to the blueprint, and setting a url prefix to be applied before the given route in the decorator.

```python
auth_bp = Blueprint("auth", __name__, 
    url_prefix='/auth',
    template_folder='auth')

@auth_bp.route("/show")
def show():
    ...
```

The URL for `show` would be `/auth/show`.

### `login()`
This view function renders the login page and will login the user.

First the form is created with `form = LoginForm()` which is injected into the page with `render_template("login.html", form=form, error=error)`.

Then we reach the user login info check
```python
if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
```

which will only pass if form data was submitted from the page by pressing the submit button. When the submit button is pressed, it sets the `validate_on_submit` flag in the `form` object on the request object to true, which allows this if check to pass.

If the form data has not been validated, meaning either the page has loaded for the first time or the submit button was not passed, then the function returns the login page

```python
return render_template("login.html", form=form, error=error)
```

If form data is validated, then the function tries to create a database object and establish a connection. If the database object fails to initialize, or if the connection fails, it will be caught by `except Exception as e:` and returns the error to be flashed on the screen.

If the database object can establish a connection, `if db.connect()`, then the username and encrypted password (see [crypto_utils.py]({{ site.baseurl }}{% link _file_details/util.md %})) are stored into the session data and the user is redirected to the index page.

### `logout()`

This will logout the user, meaning their login information is removed from the session data and then the session key is cleared.

Note that `session.clear()` will clear session data for the _current user_, but it will not clear all session data.

### `index()`
This is the home page. It doesn't have any logic, so it just returns the index html file.
