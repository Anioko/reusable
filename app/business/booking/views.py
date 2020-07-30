from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.operational.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User

booking = Blueprint('booking', __name__)


@booking.route('/')
@login_required
def index():
    """booking dashboard page."""
    return render_template('booking/index.html')
