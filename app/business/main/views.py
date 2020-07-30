import operator

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
from app.email import send_email
from .forms import *
from ...utils import Struct

main = Blueprint('main', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/home')
@login_required
def index():
    check_org_exist = db.session.query(Organisation).filter_by(user_id=current_user.id).first()
    return render_template('main/user_dashboard.html', check_org_exist=check_org_exist)

