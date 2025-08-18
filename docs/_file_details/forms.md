---
layout: page
title: Forms
nav_order: 2
---

# Forms

Forms are built using Flask-WTF forms.

Each file is a separate form.

To use a form in a page, inject the form into the html page
```python
from app.forms.login_form import LoginForm

def login():
    form = LoginForm()
    ...
    return render_template("login.html", form=form)
```
Then use jinja templating in the html file to place the form elements
{% raw %}
```jinja
{{ form.username.label }}
{{ form.username }}
{{ form.password.label }}
{{ form.password }}
{{ form.submit }}
```
{% endraw %}

All fields for forms should be field objects that are imported from `wtforms`

Common field objects:
- StringField: This is the base of most fields, accepts any text.
- PasswordField: A string field that renders characters as censored dots.
- SubmitField: Input of type "submit", acts as a normal html submit button but allows form to pass `validate_on_submit` check.
- DateTimeField: A text field that accepts a `datetime.datetime` input. Can match multiple formats, and can also explicitly define format like
```python
DateTimeField(format='%Y-%m-%d')
```
- BoolenField: Checkbox that defaults to checked.
- EmailField: Represents `<input type="email">`.
- FileField: Renders a file upload field.
- FloatField/ IntegerField: A text field that only accepts floats/ integers.
