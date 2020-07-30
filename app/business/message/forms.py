from app.models import *
from flask_ckeditor import CKEditorField
from flask_uploads import UploadSet, IMAGES
from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, StringField, SubmitField, DateField, TextAreaField, FormField, MultipleFileField, \
    RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Required, ValidationError, InputRequired, Email

images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf'))




class MessageForm(FlaskForm):
    message = StringField(('Message'), validators=[
        DataRequired(), Length(min=1, max=2500)])
    submit = SubmitField(('Submit'))


# class MessageForm(FlaskForm):
#     """ This is the messageform  """
#     body = TextAreaField('Message', validators=[Required(), Length(min=50, max=5000)])
#     submit = SubmitField('Submit')
#
# class ReplyForm(FlaskForm):
#     """ This is the message reply form  """
#     body = TextAreaField('Reply', validators=[Required(), Length(min=50, max=5000)])
#     submit = SubmitField('Submit')


