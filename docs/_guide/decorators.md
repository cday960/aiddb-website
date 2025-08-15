---
layout: page
title: Decorators
nav_order: 3
---

# Decorators

Decorators are a way to modify, extend, or restrict functions. They _wrap_ the existing function with extra behavior without editing the function's code.

```python
@custom_decorator
def do_thing():
    ...
```

The decorator `@custom_decorator` is essentially just shorthand for

```python
do_thing = my_decorator(do_thing)
```

so the decorator function recieves the original function, and returns a new function that runs the extra code before/after calling the original. That looks like this

```python
def custom_decorator(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        # 1) do something BEFORE
        result = fn(*args, **kwargs)  # call the original
        # 2) do something AFTER
        return result
    return _wrap
```

## Implementation
Looking at `auth_routes.py`, there are multiple kinds of decorators we use.

The blueprint decorators, defined by 

```python
auth_bp = Blueprint("auth", __name__)
```

assigns each view function to a route. Then once a request is made to that file, it checks each function decorator for the route that was requested, then runs the correct function once it is found.


We can also make our own custom decorators in `app/lib/decorators.py`, like `@requires_login`. Lets break this decorator down.

It starts with the normal boiler plate,

```python
def requires_login(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
```

then it checks the session data to get the user login information.

```python
        username = session.get("db_username")
        enc_pass = session.get("db_password")
```

If the username and password are not stored then the user is not logged in. If that's the case, it redirects the user to the login page.

```python
        if not username or not enc_pass:
            flash("Please log in.", "warning")
            return redirect(url_for("auth.login"))
```

Notice how this return is before we return the original function, so if this decorator is applied and the user is not logged in, __the original function never runs__. 


If the username and password exist, it tries to decrypt the password. If an exception is caught in the try except block, it again returns a redirect, preventing the original function from ever running.

```python
        try:
            # Validate password is valid
            decrypt_string(enc_pass)
        except InvalidToken:
            session.clear()
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for("auth.login"))
```

If it passes all checks, it finally returns the original function with

```python
        return fn(*args, **kwargs)
```

---

The main takeaway here is that decorators can be used to apply reusable constraints and requirements to a function before it is able to run. 

With this decorator, we never have to manually check if the user is logged in. If they should be logged in to view a page, put this decorator above the view function and that's it.

---

Decorators can get quite advanced and can help significantly reduce the amount of overhead in a codebase, so if you feel like you're writing a lot of checks for functions, maybe make it a decorator.


It is even possible to make decorators with arguments!

```python
def requires_role(role_name, source_page):
    def decorator(fn):
        @wraps(fn)
        def _wrap(*args, **kwargs):
            user_role = session.get("perm_role")
            if user_role != role_name:
                flash("Permission denied.", "warning")
                return redirect(url_for(str(source_page)))
            return fn(*args, **kwargs)
        return _wrap
    return decorator
```

This checks if a user has the appropriate permissions, and it can be used anywhere since `role_name` is passed instead of hardcoded. If they dont have permissions, it redirects them back to where they came from.
