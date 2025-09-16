from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField("Course Assign File", validators=[FileRequired()])
    submit = SubmitField("Submit")
