from flask import url_for
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
    SelectField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional
from wtforms_alchemy import model_form_factory, Unique, ModelForm
BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(BaseModelForm):
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    #photo = FileField('Profile Image', validators=[Optional(), FileAllowed(images, 'Images only!')])
    #area_code = StringField('Phone area code only', validators=[InputRequired(), Length(1, 6)])
    #mobile_phone = IntegerField('Phone numbers only', validators=[InputRequired(), Unique(User.mobile_phone)])
    #city = StringField('City', validators=[InputRequired()])
    #state = StringField(u'State or Region', validators=[Optional()])
    #profession = StringField(u'Profession',  validators=[Optional()])

    #gender = SelectField(u'Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    #zip = StringField('Zip Code', validators=[InputRequired(), Length(1, 7)])
##
##    country = SelectField(u'Select Country', choices=[
##        ('Afganistan', 'Afghanistan'),
##        ('Albania', 'Albania'),
##        ('Algeria', 'Algeria'),
##        ('American Samoa', 'American Samoa'),
##        ('Andorra', 'Andorra'),
##        ('Angola', 'Angola'),
##        ('Anguilla', 'Anguilla'),
##        ('Antigua & Barbuda', 'Antigua & Barbuda'),
##        ('Argentina', 'Argentina'),
##        ('Armenia', 'Armenia'),
##        ('Aruba', 'Aruba'),
##        ('Australia', 'Australia'),
##        ('Austria', 'Austria'),
##        ('Azerbaijan', 'Azerbaijan'),
##        ('Bahamas', 'Bahamas'),
##        ('Bahrain', 'Bahrain'),
##        ('Bangladesh', 'Bangladesh'),
##        ('Barbados', 'Barbados'),
##        ('Belarus', 'Belarus'),
##        ('Belgium', 'Belgium'),
##        ('Belize', 'Belize'),
##        ('Benin', 'Benin'),
##        ('Bermuda', 'Bermuda'),
##        ('Bhutan', 'Bhutan'),
##        ('Bolivia', 'Bolivia'),
##        ('Bonaire', 'Bonaire'),
##        ('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),
##        ('Botswana', 'Botswana'),
##        ('Brazil', 'Brazil'),
##        ('British Indian Ocean Ter', 'British Indian Ocean Ter'),
##        ('Brunei', 'Brunei'),
##        ('Bulgaria', 'Bulgaria'),
##        ('Burkina Faso', 'Burkina Faso'),
##        ('Burundi', 'Burundi'),
##        ('Cambodia', 'Cambodia'),
##        ('Cameroon', 'Cameroon'),
##        ('Canada', 'Canada'),
##        ('Canary Islands', 'Canary Islands'),
##        ('Cape Verde', 'Cape Verde'),
##        ('Cayman Islands', 'Cayman Islands'),
##        ('Central African Republic', 'Central African Republic'),
##        ('Chad', 'Chad'),
##        ('Channel Islands', 'Channel Islands'),
##        ('Chile', 'Chile'),
##        ('China', 'China'),
##        ('Christmas Island', 'Christmas Island'),
##        ('Cocos Island', 'Cocos Island'),
##        ('Colombia', 'Colombia'),
##        ('Comoros', 'Comoros'),
##        ('Congo', 'Congo'),
##        ('Cook Islands', 'Cook Islands'),
##        ('Costa Rica', 'Costa Rica'),
##        ('Cote DIvoire', 'Cote DIvoire'),
##        ('Croatia', 'Croatia'),
##        ('Cuba', 'Cuba'),
##        ('Curaco', 'Curacao'),
##        ('Cyprus', 'Cyprus'),
##        ('Czech Republic', 'Czech Republic'),
##        ('Denmark', 'Denmark'),
##        ('Djibouti', 'Djibouti'),
##        ('Dominica', 'Dominica'),
##        ('Dominican Republic', 'Dominican Republic'),
##        ('East Timor', 'East Timor'),
##        ('Ecuador', 'Ecuador'),
##        ('Egypt', 'Egypt'),
##        ('El Salvador', 'El Salvador'),
##        ('Equatorial Guinea', 'Equatorial Guinea'),
##        ('Eritrea', 'Eritrea'),
##        ('Estonia', 'Estonia'),
##        ('Ethiopia', 'Ethiopia'),
##        ('Falkland Islands', 'Falkland Islands'),
##        ('Faroe Islands', 'Faroe Islands'),
##        ('Fiji', 'Fiji'),
##        ('Finland', 'Finland'),
##        ('France', 'France'),
##        ('French Guiana', 'French Guiana'),
##        ('French Polynesia', 'French Polynesia'),
##        ('French Southern Ter', 'French Southern Ter'),
##        ('Gabon', 'Gabon'),
##        ('Gambia', 'Gambia'),
##        ('Georgia', 'Georgia'),
##        ('Germany', 'Germany'),
##        ('Ghana', 'Ghana'),
##        ('Gibraltar', 'Gibraltar'),
##        ('Great Britain', 'Great Britain'),
##        ('Greece', 'Greece'),
##        ('Greenland', 'Greenland'),
##        ('Grenada', 'Grenada'),
##        ('Guadeloupe', 'Guadeloupe'),
##        ('Guam', 'Guam'),
##        ('Guatemala', 'Guatemala'),
##        ('Guinea', 'Guinea'),
##        ('Guyana', 'Guyana'),
##        ('Haiti', 'Haiti'),
##        ('Hawaii', 'Hawaii'),
##        ('Honduras', 'Honduras'),
##        ('Hong Kong', 'Hong Kong'),
##        ('Hungary', 'Hungary'),
##        ('Iceland', 'Iceland'),
##        ('Indonesia', 'Indonesia'),
##        ('India', 'India'),
##        ('Iran', 'Iran'),
##        ('Iraq', 'Iraq'),
##        ('Ireland', 'Ireland'),
##        ('Isle of Man', 'Isle of Man'),
##        ('Israel', 'Israel'),
##        ('Italy', 'Italy'),
##        ('Jamaica', 'Jamaica'),
##        ('Japan', 'Japan'),
##        ('Jordan', 'Jordan'),
##        ('Kazakhstan', 'Kazakhstan'),
##        ('Kenya', 'Kenya'),
##        ('Kiribati', 'Kiribati'),
##        ('Korea North', 'Korea North'),
##        ('Korea Sout', 'Korea South'),
##        ('Kuwait', 'Kuwait'),
##        ('Kyrgyzstan', 'Kyrgyzstan'),
##        ('Laos', 'Laos'),
##        ('Latvia', 'Latvia'),
##        ('Lebanon', 'Lebanon'),
##        ('Lesotho', 'Lesotho'),
##        ('Liberia', 'Liberia'),
##        ('Libya', 'Libya'),
##        ('Liechtenstein', 'Liechtenstein'),
##        ('Lithuania', 'Lithuania'),
##        ('Luxembourg', 'Luxembourg'),
##        ('Macau', 'Macau'),
##        ('Macedonia', 'Macedonia'),
##        ('Madagascar', 'Madagascar'),
##        ('Malaysia', 'Malaysia'),
##        ('Malawi', 'Malawi'),
##        ('Maldives', 'Maldives'),
##        ('Mali', 'Mali'),
##        ('Malta', 'Malta'),
##        ('Marshall Islands', 'Marshall Islands'),
##        ('Martinique', 'Martinique'),
##        ('Mauritania', 'Mauritania'),
##        ('Mauritius', 'Mauritius'),
##        ('Mayotte', 'Mayotte'),
##        ('Mexico', 'Mexico'),
##        ('Midway Islands', 'Midway Islands'),
##        ('Moldova', 'Moldova'),
##        ('Monaco', 'Monaco'),
##        ('Mongolia', 'Mongolia'),
##        ('Montserrat', 'Montserrat'),
##        ('Morocco', 'Morocco'),
##        ('Mozambique', 'Mozambique'),
##        ('Myanmar', 'Myanmar'),
##        ('Nambia', 'Nambia'),
##        ('Nauru', 'Nauru'),
##        ('Nepal', 'Nepal'),
##        ('Netherland Antilles', 'Netherland Antilles'),
##        ('Netherlands', 'Netherlands (Holland, Europe)'),
##        ('Nevis', 'Nevis'),
##        ('New Caledonia', 'New Caledonia'),
##        ('New Zealand', 'New Zealand'),
##        ('Nicaragua', 'Nicaragua'),
##        ('Niger', 'Niger'),
##        ('Nigeria', 'Nigeria'),
##        ('Niue', 'Niue'),
##        ('Norfolk Island', 'Norfolk Island'),
##        ('Norway', 'Norway'),
##        ('Oman', 'Oman'),
##        ('Pakistan', 'Pakistan'),
##        ('Palau Island', 'Palau Island'),
##        ('Palestine', 'Palestine'),
##        ('Panama', 'Panama'),
##        ('Papua New Guinea', 'Papua New Guinea'),
##        ('Paraguay', 'Paraguay'),
##        ('Peru', 'Peru'),
##        ('Phillipines', 'Philippines'),
##        ('Pitcairn Island', 'Pitcairn Island'),
##        ('Poland', 'Poland'),
##        ('Portugal', 'Portugal'),
##        ('Puerto Rico', 'Puerto Rico'),
##        ('Qatar', 'Qatar'),
##        ('Republic of Montenegro', 'Republic of Montenegro'),
##        ('Republic of Serbia', 'Republic of Serbia'),
##        ('Reunion', 'Reunion'),
##        ('Romania', 'Romania'),
##        ('Russia', 'Russia'),
##        ('Rwanda', 'Rwanda'),
##        ('St Barthelemy', 'St Barthelemy'),
##        ('St Eustatius', 'St Eustatius'),
##        ('St Helena', 'St Helena'),
##        ('St Kitts-Nevis', 'St Kitts-Nevis'),
##        ('St Lucia', 'St Lucia'),
##        ('St Maarten', 'St Maarten'),
##        ('St Pierre & Miquelon', 'St Pierre & Miquelon'),
##        ('St Vincent & Grenadines', 'St Vincent & Grenadines'),
##        ('Saipan', 'Saipan'),
##        ('Samoa', 'Samoa'),
##        ('Samoa American', 'Samoa American'),
##        ('San Marino', 'San Marino'),
##        ('Sao Tome & Principe', 'Sao Tome & Principe'),
##        ('Saudi Arabia', 'Saudi Arabia'),
##        ('Senegal', 'Senegal'),
##        ('Seychelles', 'Seychelles'),
##        ('Sierra Leone', 'Sierra Leone'),
##        ('Singapore', 'Singapore'),
##        ('Slovakia', 'Slovakia'),
##        ('Slovenia', 'Slovenia'),
##        ('Solomon Islands', 'Solomon Islands'),
##        ('Somalia', 'Somalia'),
##        ('South Africa', 'South Africa'),
##        ('Spain', 'Spain'),
##        ('Sri Lanka', 'Sri Lanka'),
##        ('Sudan', 'Sudan'),
##        ('Suriname', 'Suriname'),
##        ('Swaziland', 'Swaziland'),
##        ('Sweden', 'Sweden'),
##        ('Switzerland', 'Switzerland'),
##        ('Syria', 'Syria'),
##        ('Tahiti', 'Tahiti'),
##        ('Taiwan', 'Taiwan'),
##        ('Tajikistan', 'Tajikistan'),
##        ('Tanzania', 'Tanzania'),
##        ('Thailand', 'Thailand'),
##        ('Togo', 'Togo'),
##        ('Tokelau', 'Tokelau'),
##        ('Tonga', 'Tonga'),
##        ('Trinidad & Tobago', 'Trinidad & Tobago'),
##        ('Tunisia', 'Tunisia'),
##        ('Turkey', 'Turkey'),
##        ('Turkmenistan', 'Turkmenistan'),
##        ('Turks & Caicos Is', 'Turks & Caicos Is'),
##        ('Tuvalu', 'Tuvalu'),
##        ('Uganda', 'Uganda'),
##        ('United Kingdom', 'United Kingdom'),
##        ('Ukraine', 'Ukraine'),
##        ('United Arab Erimates', 'United Arab Emirates'),
##        ('United States of America', 'United States of America'),
##        ('Uraguay', 'Uruguay'),
##        ('Uzbekistan', 'Uzbekistan'),
##        ('Vanuatu', 'Vanuatu'),
##        ('Vatican City State', 'Vatican City State'),
##        ('Venezuela', 'Venezuela'),
##        ('Vietnam', 'Vietnam'),
##        ('Virgin Islands (Brit)', 'Virgin Islands (Brit)'),
##        ('Virgin Islands (USA)', 'Virgin Islands (USA)'),
##        ('Wake Island', 'Wake Island'),
##        ('Wallis & Futana Is', 'Wallis & Futana Is'),
##        ('Yemen', 'Yemen'),
##        ('Zaire', 'Zaire'),
##        ('Zambia', 'Zambia'),
##        ('Zimbabwe', 'Zimbabwe')])
##    #summary_text = TextAreaField('Summary Text or Description')

    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. (Did you mean to '
                                  '<a href="{}">log in</a> instead?)'.format(url_for('account.login')))



class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Reset password')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Set password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class ChangeProfileForm(BaseModelForm):
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    summary_text = TextAreaField('Summary Text or Description')
    photo = FileField('Profile Image', validators=[Optional(), FileAllowed(images, 'Images only!')])
    area_code = StringField('Phone area code only', validators=[InputRequired()])
    mobile_phone = IntegerField('Phone numbers only', validators=[InputRequired(), Unique(User.mobile_phone)])
    city = StringField('City', validators=[InputRequired()])
    state = StringField(u'State', validators=[Optional()])

    profession = StringField(u'Profession', validators=[Optional()])
    gender = SelectField(u'Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    zip = StringField('Zip Code', validators=[InputRequired(), Length(1, 7)])
    country = SelectField(u'Select Country', choices=[
        ('Afganistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antigua & Barbuda', 'Antigua & Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bermuda', 'Bermuda'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bonaire', 'Bonaire'),
        ('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('British Indian Ocean Ter', 'British Indian Ocean Ter'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Canary Islands', 'Canary Islands'),
        ('Cape Verde', 'Cape Verde'),
        ('Cayman Islands', 'Cayman Islands'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Channel Islands', 'Channel Islands'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Christmas Island', 'Christmas Island'),
        ('Cocos Island', 'Cocos Island'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Costa Rica', 'Costa Rica'),
        ('Cote DIvoire', 'Cote DIvoire'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Curaco', 'Curacao'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic', 'Czech Republic'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor', 'East Timor'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Falkland Islands', 'Falkland Islands'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('French Guiana', 'French Guiana'),
        ('French Polynesia', 'French Polynesia'),
        ('French Southern Ter', 'French Southern Ter'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Great Britain', 'Great Britain'),
        ('Greece', 'Greece'),
        ('Greenland', 'Greenland'),
        ('Grenada', 'Grenada'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Hawaii', 'Hawaii'),
        ('Honduras', 'Honduras'),
        ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('Indonesia', 'Indonesia'),
        ('India', 'India'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Isle of Man', 'Isle of Man'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea North', 'Korea North'),
        ('Korea Sout', 'Korea South'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Macau', 'Macau'),
        ('Macedonia', 'Macedonia'),
        ('Madagascar', 'Madagascar'),
        ('Malaysia', 'Malaysia'),
        ('Malawi', 'Malawi'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Martinique', 'Martinique'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'),
        ('Mexico', 'Mexico'),
        ('Midway Islands', 'Midway Islands'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montserrat', 'Montserrat'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar', 'Myanmar'),
        ('Nambia', 'Nambia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherland Antilles', 'Netherland Antilles'),
        ('Netherlands', 'Netherlands (Holland, Europe)'),
        ('Nevis', 'Nevis'),
        ('New Caledonia', 'New Caledonia'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'),
        ('Norfolk Island', 'Norfolk Island'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau Island', 'Palau Island'),
        ('Palestine', 'Palestine'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Phillipines', 'Philippines'),
        ('Pitcairn Island', 'Pitcairn Island'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Qatar', 'Qatar'),
        ('Republic of Montenegro', 'Republic of Montenegro'),
        ('Republic of Serbia', 'Republic of Serbia'),
        ('Reunion', 'Reunion'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('St Barthelemy', 'St Barthelemy'),
        ('St Eustatius', 'St Eustatius'),
        ('St Helena', 'St Helena'),
        ('St Kitts-Nevis', 'St Kitts-Nevis'),
        ('St Lucia', 'St Lucia'),
        ('St Maarten', 'St Maarten'),
        ('St Pierre & Miquelon', 'St Pierre & Miquelon'),
        ('St Vincent & Grenadines', 'St Vincent & Grenadines'),
        ('Saipan', 'Saipan'),
        ('Samoa', 'Samoa'),
        ('Samoa American', 'Samoa American'),
        ('San Marino', 'San Marino'),
        ('Sao Tome & Principe', 'Sao Tome & Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Tahiti', 'Tahiti'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'),
        ('Trinidad & Tobago', 'Trinidad & Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Turks & Caicos Is', 'Turks & Caicos Is'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('United Kingdom', 'United Kingdom'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Erimates', 'United Arab Emirates'),
        ('United States of America', 'United States of America'),
        ('Uraguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City State', 'Vatican City State'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands (Brit)', 'Virgin Islands (Brit)'),
        ('Virgin Islands (USA)', 'Virgin Islands (USA)'),
        ('Wake Island', 'Wake Island'),
        ('Wallis & Futana Is', 'Wallis & Futana Is'),
        ('Yemen', 'Yemen'),
        ('Zaire', 'Zaire'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe')])

    submit = SubmitField('Update')
