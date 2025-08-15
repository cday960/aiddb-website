---
layout: page
title: "Example Logic Flow"
nav_order: 3
---

# Example Logic Flow

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

