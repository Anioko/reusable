from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
import commonmark
from app import db
from app.decorators import admin_required
from app.models import Message
from app.operational.admin.views import admin
from wtforms import Flags
#from .forms import PostForm, CategoryForm, EditCategoryForm






@admin.route('/messages', defaults={'page': 1}, methods=['GET'])
@admin.route('/messages/<int:page>', methods=['GET'])
@login_required
@admin_required
def messages(page):
    messages_result = Message.query.paginate(page, per_page=100)
    return render_template('admin/messages/browse.html', messages=messages_result)


@admin.route('/message/<int:message_id>/_delete', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    message = Message.query.filter_by(id=message_id).first()
    db.session.delete(message)
    db.session.commit()
    flash('Successfully deleted Message.', 'success')
    return redirect(url_for('admin.messages'))
