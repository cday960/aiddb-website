from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField("Course Assign File", validators=[FileRequired()])
    # submit = SubmitField("Upload File")
    missing_course_grade_level = SubmitField("Missing CourseGradeLevel")
    missing_edssn = SubmitField("Missing EDSSN")
    missing_course_num = SubmitField("Missing CourseNum")
    missing_course_sem = SubmitField("Missing CourseSem")
    duplicate_assign_num = SubmitField("Duplicate AssignNum")


class ToolForm(FlaskForm):
    tool = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Run tool")
