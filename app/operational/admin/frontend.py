from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
import commonmark
from app import db
from app.decorators import admin_required
from app.models import EditableHTML, Role, User, Organisation, Message, ContactMessage, LandingSetting, LandingImage, OurBrand
from app.operational.admin.views import admin
from wtforms import Flags
from .forms import (
    LandingSettingForm,
    LandingImageForm,
    OurBrandForm
    
)

from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed

images = UploadSet('images', IMAGES)
photos = UploadSet('photos', IMAGES)




@admin.route('/settings/dashboard/')
@login_required
@admin_required
def frontend_dashboard():
    """Frontend dashboard page."""
    return render_template('admin/frontend_settings_dashboard.html')

@admin.route('/landing-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def landing_setting(id=None):
    """Adds information to the landing page."""
    settings = db.session.query(LandingSetting.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_landing_setting', id=1))
    form = LandingSettingForm()
    if request.method == 'POST':
            settings = LandingSetting(
                site_name = form.site_name.data,
                title = form.title.data,
                description = form.description.data,
                
                twitter_name = form.twitter_name.data,
                facebook_name = form.facebook_name.data,
                instagram_name=form.instagram_name.data,
                linkedin_name = form.linkedin_name.data,
                tiktok_name = form.tiktok_name.data,
                snap_chat_name = form.snap_chat_name.data,
                youtube = form.youtube.data,
                blog = form.blog.data,
                about = form.about.data,
                contact = form.contact.data,
                
                faq = form.faq.data,
                
                featured_title_one = form.featured_title_one.data,
                featured_title_one_text = form.featured_title_one_text.data,
                featured_title_one_icon = form.featured_title_one_icon.data,
                featured_title_two = form.featured_title_two.data,
                featured_title_two_text = form.featured_title_two_text.data,
                featured_title_two_icon = form.featured_title_two_icon.data,
                featured_title_three = form.featured_title_three.data,
                featured_title_three_text = form.featured_title_three_text.data,
                featured_title_three_icon = form.featured_title_three_icon.data,
                
                google_analytics_id = form.google_analytics_id.data,
                other_tracking_analytics_one = form.other_tracking_analytics_one.data,
                other_tracking_analytics_two = form.other_tracking_analytics_two.data,
                block_content_one = form.block_content_one.data
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_landing_setting', id=id))
    return render_template('admin/new_landing_setting.html', form=form)

@admin.route('/edit-landing-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_landing_setting(id):
    """Edit information to the landing page."""
    settings = LandingSetting.query.get(id)
    form = LandingSettingForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_landing_setting.html', form=form)


@admin.route('/upload', methods=['GET', 'POST'])
def upload():
    form = LandingImageForm()
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        image = LandingImage(image=image)
        db.session.add(image)
        db.session.commit()
        flash("Photo saved.")
        return redirect(url_for('admin.show', id=image.id))
    return render_template('admin/upload.html', form=form)

@admin.route('/image/<int:id>')
def show(id):
    photo = LandingImage.query.get(id)
    if photo is None:
        abort(404)
    url = images.url(photo.image)
    return render_template('admin/show.html', url=url, photo=photo)


@admin.route('/landing-brand-settings', methods=['GET', 'POST'])
@admin.route('/landing-brand-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def landing_brand_setting(id=None):
    """Adds information to the landing page."""
    settings = db.session.query(OurBrand.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_landing_brand_setting', id=1))
    form = OurBrandForm()
    if request.method == 'POST':
            settings = OurBrand(

                brand_name_one = form.brand_name_one.data,
                brand_name_two = form.brand_name_two.data,
                brand_name_three = form.brand_name_three.data,
                brand_name_five = form.brand_name_five.data,
                brand_url_one = form.brand_url_five.data,
                brand_url_two = form.brand_url_five.data,
                brand_url_three = form.brand_url_five.data,
                brand_url_four = form.brand_url_five.data,
                brand_url_five = form.brand_url_five.data
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_landing_brand_setting', id=id))
    return render_template('admin/new_landing_brand_setting.html', form=form)


@admin.route('/edit-landing-brand-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_landing_brand_setting(id):
    """Edit information to the landing page."""
    settings = OurBrand.query.get(id)
    form = OurBrandForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/new_landing_brand_setting.html', form=form)

@admin.route('/landing-news-settings', methods=['GET', 'POST'])
@admin.route('/landing-news-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def landing_news_setting(id=None):
    """Adds information to the landing page."""
    settings = db.session.query(NewsLink.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_landing_brand_setting', id=1))
    form = NewsLinkForm()
    if request.method == 'POST':
            settings = NewsLink(

                news_site_one = form.news_site_one.data,
                news_site_two = form.news_site_two.data,
                news_site_three = form.news_site_three.data,
                news_site_five = form.news_site_five.data,
                news_url_one = form.news_url_five.data,
                news_url_two = form.news_url_five.data,
                news_url_three = form.news_url_five.data,
                news_url_four = form.news_url_five.data,
                news_url_five = form.news_url_five.data
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_landing_brand_setting', id=id))
    return render_template('admin/new_landing_edit_setting.html', form=form)


@admin.route('/edit-landing-brand-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_landing_news_setting(id):
    """Edit information to the landing page."""
    settings = NewsLink.query.get(id)
    form = NewsLinkForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/new_landing_edit_setting.html', form=form)
