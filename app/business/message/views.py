import operator

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_ckeditor import upload_success
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
from app.email import send_email
from .forms import *
from ...utils import Struct
from app.models import *

message = Blueprint('message', __name__)






@message.route('/conversation/<recipient>/<full_name>', methods=['GET', 'POST'])
@login_required
def send_message(recipient, full_name):
    user = User.query.filter(User.id != current_user.id).filter_by(id=recipient).first_or_404()
    for message in current_user.history(user.id):
        if message.recipient_id == current_user.id:
            message.read_at = db.func.now()
        db.session.add(message)
    db.session.commit()
    form = MessageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message(user_id=current_user.id, recipient=user,
                          body=form.message.data)
            db.session.add(msg)
            db.session.commit()
            user.add_notification('unread_message', {'message': msg.id, 'count': user.new_messages()},
                                  related_id=current_user.id, permanent=True)
            flash('Your message has been sent.')
            return redirect(url_for('notification.send_message', recipient=user.id, full_name=user.full_name))
    follow_lists = User.query.filter(User.id != current_user.id).order_by(func.random()).limit(10).all()
    jobs = Job.query.filter(Job.organisation != None).filter(Job.end_date >= datetime.now()).order_by(
        Job.pub_date.asc()).all()
    return render_template('message/send_messages.html', title='Send Message',
                           form=form, recipient=user, current_user=current_user, follow_lists=follow_lists, jobs=jobs)



@message.route('/conversations', defaults={'page': 1}, methods=['GET'])
@message.route('/conversations/<page>', methods=['GET'])
@login_required
def conversations(page):
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
        page, 10, False)
    conversations = Message.query.filter(
        or_(Message.user_id == current_user.id, Message.recipient_id == current_user.id)).all()
    user_ids = [conversation.user_id for conversation in conversations] + [conversation.recipient_id for conversation in
                                                                           conversations]
    user_ids = list(set(user_ids))
    if current_user.id in user_ids:
        user_ids.remove(current_user.id)
    users = User.query.filter(User.id.in_(user_ids)).paginate(page, per_page=20)
    return render_template('main/messages.html', messages=messages.items, users=users)
