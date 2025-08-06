from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("DB Username", validators=[DataRequired()])
    password = PasswordField("DB Password", validators=[DataRequired()])
    submit = SubmitField("Login")
