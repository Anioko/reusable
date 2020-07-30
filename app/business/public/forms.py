from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms import StringField, SelectField, DateTimeField, IntegerField, TextAreaField
#from app.wtform_widgets import MarkdownField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length
from flask_wtf import Form

#from app.models import User


class SiteSettingForm(FlaskForm):
    site_title = StringField("Site Title", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    siteaddress=StringField("Site Address",validators=[InputRequired(), \
                        Length(min=1, max=128)])
    administration_user_address=StringField("Site Administration User Address",validators=[InputRequired(), \
                        Length(min=1, max=128)])
    site_Language=StringField("Site Language",validators=[InputRequired(), \
                        Length(min=1, max=128)])
    submit = SubmitField('Submit')
    


class ContactForm(FlaskForm):
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')

class PublicContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')
