from flask_ckeditor import CKEditorField
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    DecimalField,
    FloatField,
    FileField,
    BooleanField,
    MultipleFileField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional
from wtforms_alchemy import Unique, ModelForm, model_form_factory

from app import db
from app.models import *

images = UploadSet('images', IMAGES)
BaseModelForm = model_form_factory(FlaskForm)

#####Payment Forms Starts #####

class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


#####User Forms Ends #####
#####Payment Forms Start #####

class PaymentSettingForm(FlaskForm):

    name = StringField("Stripe Public Key or Public Key",validators=[InputRequired()])
    display_name = StringField("Display Name")
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

#####Payment Forms Ends #####

#####Payment Forms Start #####

class PricingPlanForm(FlaskForm):

    name = StringField("Free or Basic or Pro or Gold",validators=[InputRequired()])
    duration = IntegerField("Number of days. E.g: 30", validators=[InputRequired()])
    cost = DecimalField("Cost e.g 0.00")
    currency_symbol = StringField("symbol")
    submit = SubmitField('Submit')


#####Payment Forms Ends #####


#####Transactionfee Forms Start #####

class TransactionFeeForm(FlaskForm):

    provider_name = StringField("Stripe or Paystack",validators=[InputRequired()])
    local_fee = IntegerField("Local Fee's. E.g: 100", validators=[InputRequired()])
    european_fee = IntegerField("European Fee's. E.g: 100")
    international_fee = IntegerField("International Fee's. E.g: 100", validators=[InputRequired()])
    our_fee = IntegerField("Our fee. E.g: 100", validators=[InputRequired()])
    transfer_fee = DecimalField("Provider's money transfer fee. E.g: 100", validators=[InputRequired()])
    local_percentage = DecimalField("Local percentage per transaction e.g 1.50")
    european_percentage = DecimalField("European percentage per transaction e.g 1.50")
    international_percentage = DecimalField("International percentage per transaction e.g 1.50")
    our_percentage = DecimalField("Our percentage per transaction e.g 1.50")
    currency_symbol = StringField("Currency Symbol",validators=[InputRequired()])
    submit = SubmitField('Submit')


#####Payment Forms Ends #####
    
#####Marketplace Forms Starts #####

class MCategoryForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    order = IntegerField('Order', validators=[InputRequired()])
    is_featured = BooleanField("Is Featured ?")
    parent = QuerySelectField(
        'Parent Category',
        get_label='name',
        allow_blank=True,
        blank_text="No Parent",
        query_factory=lambda: db.session.query(MCategory).filter_by(parent_id=None).order_by('name'))
    submit = SubmitField('Submit')



class MCurrencyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    symbol = StringField('Symbol', validators=[InputRequired()])
    default = BooleanField('Is Default ?')
    submit = SubmitField('Submit')


class MShippingMethodForm(FlaskForm):
    seller = QuerySelectField(
        'Seller',
        validators=[InputRequired()],
        get_label='full_name',
        query_factory=lambda: db.session.query(User).filter_by(is_seller=True).order_by('first_name'))
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class MProductForm(FlaskForm):
    name = StringField('Product name', validators=[InputRequired(), Length(1, 64)])
    images = MultipleFileField('Product Images', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    description = TextAreaField('Description', [InputRequired()])
    categories = QuerySelectMultipleField(
        'Categories',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(MCategory).order_by('order'))
    availability = BooleanField(u'Is it currently available?')
    min_order_quantity = IntegerField('Min number of units per order e.g 1', default=1)
    length = FloatField('Length in numbers only e.g 0.99')
    weight = FloatField('Weight in numbers only e.g 0.21')
    height = FloatField('Height in numbers only e.g 10')
    price = FloatField('Price, Figures only e.g 16.99')
    seller = QuerySelectField(
        'Seller',
        validators=[InputRequired()],
        get_label='full_name',
        query_factory=lambda: db.session.query(User).filter_by(is_seller=True).order_by('first_name'))
    price_currency = QuerySelectField(
        'Price currency',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(MCurrency).order_by('name'))
    is_featured = BooleanField("Is Featured ?")
    lead_time = StringField('Delivery time')
    submit = SubmitField('Submit')

#####Forms Ends #####
#####Blog Forms Starts #####
class BlogCategoryForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    order = IntegerField('Order', validators=[InputRequired()])
    is_featured = BooleanField("Is Featured ?")
    submit = SubmitField('Submit')


class BlogTagForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class BlogNewsLetterForm(BaseModelForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email(), Unique(BlogNewsLetter.email)])
    submit = SubmitField('Submit')


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    text = CKEditorField('Body', validators=[InputRequired()])
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    categories = QuerySelectMultipleField(
        'Categories',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogCategory).order_by('order'))
    tags = QuerySelectMultipleField(
        'Tags',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogTag).order_by('created_at'))
    newsletter = BooleanField('Send Announcement To Subscribers.')
    all_users = BooleanField('Send Announcement To All Users.')

    submit = SubmitField('Submit')

#####Forms Ends #####
#####Frontend Forms Starts #####
class LandingSettingForm(FlaskForm):
    site_name = StringField('Site Name e.g bookstore.ng', validators=[InputRequired(), Length(1, 128)])
    title = StringField('Website Title', validators=[InputRequired(), Length(1, 128)])
    description = StringField('Website description', validators=[InputRequired(), Length(1, 180)])
    twitter_name = StringField('Twitter accname only')
    facebook_name = StringField('Facebook pagename only')
    instagram_name = StringField('Instagram username only')
    tiktok_name = StringField('Tiktok username only')
    linkedin_name = StringField('Linkedin pagename only')
    snap_chat_name = StringField('Snap chat username only')
    youtube = StringField('Youtube page name only')
    blog = StringField('e.g blog')
    about = StringField('e.g about')
    contact = StringField('e.g contact')
    faq = StringField('e.g faq')
    
    logo = FileField('Logo', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    #images = MultipleFileField('Images', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    h1 = StringField('H1 text', validators=[InputRequired(), Length(1, 180)])
    h2 = StringField('H2 Text')
    h3 = StringField('H3 Text')
    h4 = StringField('H4 Text')
    h5 = StringField('H5 Text')
  
    featured_title_one = StringField('e.g Fast delivery')
    featured_title_one_text = StringField('Write about 90 words')
    featured_title_one_icon = StringField('e.g fa-truck')
    featured_title_two = StringField('e.g Creative Strategy')
    featured_title_two_text = StringField('Write about 90 words')
    featured_title_two_icon = StringField('e.g fa-landmark')
    featured_title_three = StringField('e.g High secured')
    featured_title_three_text = StringField('Write about 90 words')
    featured_title_three_icon = StringField('e.g fa-lock')
    
    google_analytics_id = StringField('Google Analytics ID')
    other_tracking_analytics_one = StringField('Insert Analytics Script')
    other_tracking_analytics_two = StringField('Insert Analytics Script')
    other_tracking_analytics_three = StringField('Insert Analytics Script')
    other_tracking_analytics_four = StringField('Insert Analytics Script')
    block_content_one = TextAreaField('Description')
    html_code_one = TextAreaField('Insert raw html')
    html_code_two = TextAreaField('Insert raw html')
    html_code_three = TextAreaField('Insert raw html')
    html_code_four = TextAreaField('Insert raw html')
    submit = SubmitField('Submit')

class LandingImageForm(FlaskForm):

    image = FileField('Image', validators=[Optional(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')

class OurBrandForm(FlaskForm):
    ### these are brands which we own in house
    
    brand_name_one = StringField('e.g Mediville')
    brand_name_two = StringField('e.g Networkedng')
    brand_name_three = StringField('e.g Intel')
    brand_name_four = StringField('e.g teamsworkspace')
    brand_name_five = StringField('e.g teamsworkspace')
    brand_url_one = StringField('e.g mediville.com')
    brand_url_two = StringField('e.g https://networked.ng')
    brand_url_three = StringField('e.g http://intel.com')
    brand_url_four = StringField('e.g teamsworkspace.com.ng')
    brand_url_five = StringField('e.g https://teamsworkspace.com.ng')
    submit = SubmitField('Submit')

class NewsLinkForm(FlaskForm):
    ### these are news sites that write about us
    
    news_site_one = StringField('e.g CNN')
    news_site_two = StringField('e.g BBC')
    news_site_three = StringField('e.g FoxNews')
    news_site_four = StringField('e.g PunchNews')
    news_site_five = StringField('e.g Vanguard')
    news_url_one = StringField('e.g cnn.com/link_to_news')
    news_url_two = StringField('e.g https://bbc.com/link_to_news')
    news_url_three = StringField('e.g http://foxnews.com/link_to_news')
    news_url_four = StringField('e.g punch.ng/link_to_news')
    news_url_five = StringField('e.g https://vanguard.com/link_to_news')
    submit = SubmitField('Submit')

