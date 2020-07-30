from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
import commonmark
from app import db
from app.decorators import admin_required
from app.models import Organisation
from app.operational.admin.views import admin
from wtforms import Flags
#from .forms import PostForm, CategoryForm, EditCategoryForm






@admin.route('/orgs', defaults={'page': 1}, methods=['GET'])
@admin.route('/orgs/<int:page>', methods=['GET'])
@login_required
@admin_required
def orgs(page):
    orgs = Organisation.query.paginate(page, per_page=100)
    return render_template('admin/orgs/browse.html', orgs=orgs)


@admin.route('/org/<int:org_id>/_delete', methods=['POST'])
@login_required
@admin_required
def delete_org(org_id):
    org = Organisation.query.filter_by(id=org_id).first()
    db.session.delete(org)
    db.session.commit()
    flash('Successfully deleted Organisation.', 'success')
    return redirect(url_for('admin.orgs'))
