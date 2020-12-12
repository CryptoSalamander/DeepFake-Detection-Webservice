from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class VideoUploadForm(FlaskForm):

    video_content = FileField('영상', validators=[ FileAllowed(
        ['mp4', 'mkv', '3gp', 'mov']), FileRequired()])
    submit = SubmitField("업로드")
