from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import *
from .forms import SiteSettingForm
import commonmark
from app import db
from app.decorators import admin_required

#from .forms import PostForm, CategoryForm, EditCategoryForm
public = Blueprint('public', __name__)



@public.route('/')
def index():
    settings = LandingSetting.query.all()
    brands = OurBrand.query.all()
    newslinks = NewsLink.query.all()
    categories_instances = MCategory.query.filter_by(is_featured=True).all()
    products = MProduct.query.filter_by(availability=True).filter_by(is_featured=True).all()
    public = SiteSetting.query.limit(1).all()
    if current_user.is_authenticated:
        return redirect(url_for('marketplace.index'))
    else:
        return render_template('public/page-index-1.html', settings=settings, brands=brands,
                               newslinks=newslinks, current_user=current_user, categories=categories_instances,
                               products=products, public=public)


@public.route('/all')
@login_required
@admin_required
def site_public():
    all_public = SiteSetting.query.order_by(SiteSetting.id).all()
    return render_template("public/index.html",
                           public=all_public)


@public.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_site_setting(id):
    form = SiteSettingForm()

    site_setting = db.session.query(SiteSetting).filter(SiteSetting.id==id).first()

    if(site_setting is None):
        abort(404)

    if form.validate_on_submit():
        site_setting.site_title = form.site_title.data
        site_setting.siteaddress= form.siteaddress.data
        site_setting.administration_user_address=form.administration_user_address.data
        site_setting.site_Language = form.site_Language.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.site_title))

        return redirect(url_for('public.site_public'))

    form.site_title.data = site_setting.site_title
    form.siteaddress.data = site_setting.siteaddress
    form.administration_user_address.data= site_setting.administration_user_address
    form.site_Language.data=site_setting.site_Language

    return render_template("public/edit.html", form=form,
                           setting=site_setting)


@public.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_site_setting():
    check_data_exists = SiteSetting.query.get(1)

    #if check_data_exists is  None :
       #return redirect(url_for('public.edit_site_setting',id=id))
    form = SiteSettingForm()

    if form.validate_on_submit():
        site_setting = SiteSetting()
        site_setting.site_title = form.site_title.data
        site_setting.siteaddress = form.siteaddress.data
        site_setting.administration_user_address =form.administration_user_address.data
        site_setting.site_Language = form.site_Language.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.site_title))

        return redirect(url_for('public.site_public'))

    return render_template("public/new.html", form=form)


@public.route('/delete/<int:id>')
@login_required
@admin_required
def delete_site_setting(id):
    setting = SiteSetting.query.filter_by(id=id).first()

    if(setting is not None):
        db.session.delete(setting)

        flash('"{0}" has been deleted.'.format(setting.site_title))
        return redirect(url_for('public.site_public'))

    flash('Setting does not exist')
    return redirect(url_for('public.site_public'))


@public.route('/about')
def about():
    public = SiteSetting.find_all()
    return render_template("public/about.html",public=public)

@public.route('/privacy')
def privacy():
    editable_html_obj = EditableHTML.get_editable_html('privacy')
    return render_template('public/privacy.html', editable_html_obj=editable_html_obj)


@public.route('/terms')
def terms():
    editable_html_obj = EditableHTML.get_editable_html('terms')
    return render_template('public/terms.html', editable_html_obj=editable_html_obj)


@public.route('/faq')
def faq():
    editable_html_obj = EditableHTML.get_editable_html('faq')
    return render_template('public/faq.html', editable_html_obj=editable_html_obj)


