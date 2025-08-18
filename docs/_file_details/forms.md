---
layout: page
title: Forms
nav_order: 2
---

# Forms

Forms are built using Flask-WTF forms.

Each file is a separate form.

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
