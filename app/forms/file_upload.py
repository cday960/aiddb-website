from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField("Course Assign File", validators=[FileRequired()])
    submit = SubmitField("Upload File")


class ToolForm(FlaskForm):
    tool = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Run tool")
