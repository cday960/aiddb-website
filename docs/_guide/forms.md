---
layout: page
title: Forms
nav_order: 1
---

# Forms

Structured forms are how user input is sanitized and trusted. This webapp utilizes Flask_WTF which lets us integrate WTForms in Flask. WTForms is a simple data validation library to make sure users aren't putting js scripts into their username box, among other nefarious things.

## Field Objects
Forms are established in `website/app/forms`, and each form will get a new file. In `login_form.py` there is a class, `LoginForm`, which extends the `FlaskForm` class. Then the attributes of the class are just whatever fields you want that form to have. 
Since this is a login form we need a username, password, and submit button. 
- Username is a normal text field, so we use the `StringField`.
- Password, we want the characters hidden on screen so we use the `PasswordField` object, etc. 
- Submit button, `SubmitField` object packages the form data into headers before resubmitting the request to the url of the page it is on. The `if` block only runs if the data is validated (the button press is what sent the request).
All field objects are listed in great length on the [FlaskWTF docs](https://flask-wtf.readthedocs.io/en/1.2.x/#:~:text=Flask%2DWTF%20%E2%80%94%20Flask%2DWTF,Version%200.10.3).


## Validators
Validators verify that the input fits a set of criteria based off what validator object is used. The `DataRequired` object ensures the field is not empty on submit. More specifically, it checks that `form.<field>.data` exists. This is important since in the `if` block in `app/routes/auth_routes.py` we assign username and password to the form data, which wouldn't be possible if the login fields were left empty. Validators should always be used.
- [Validator Docs](https://wtforms.readthedocs.io/en/2.3.x/validators/)


## Rendering in HTML
The form object is passed to the `render_template` function so it can be placed in the html file.

Use Jinja templating to place the passed form as html elements.

{% raw %}
```jinja
{{ form.username.label }}
{{ form.username }}
{{ form.password.label }}
{{ form.password }}
{{ form.submit }}
```
{% endraw %}

Every single form should (I hope...) follow this structure with little deviation.

## Jinja
- [Official Docs](https://jinja.palletsprojects.com/en/stable/)
- [GeeksForGeeks article](https://www.geeksforgeeks.org/python/templating-with-jinja2-in-flask/)
Official docs are good for syntax, gfg article lists all info you should need to make new pages for this webapp.
