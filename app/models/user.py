import json
import os

import cv2
from datetime import datetime
from logging import log
from time import time

import socketio
from flask import current_app, url_for
from flask_jwt_extended import create_access_token
from flask_login import AnonymousUserMixin, UserMixin, current_user
from flask_rq import get_queue
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey, or_, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, make_transient_to_detached
from sqlalchemy_mptt.mixins import BaseNestedSets
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils import pretty_date, db, login_manager, jsonify_object
from .message import Message
from flask_whooshee import Whooshee


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name

@whooshee.register_model('profession', 'summary_text', 'first_name', 'last_name', 'city', 'state', 'country')
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    is_seller = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    gender = db.Column(db.String(64), index=True)
    profession = db.Column(db.String(64), index=True)
    area_code = db.Column(db.String(6), index=True)
    mobile_phone = db.Column(db.BigInteger, unique=True, index=True)
    summary_text = db.Column(db.Text)
    zip = db.Column(db.String(10), index=True)
    city = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    socket_id = db.Column(db.Text())
    online = db.Column(db.String(1), default='N')
    invited_by = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete="CASCADE"))
    photos = db.relationship('Photo', backref='user',
                             lazy='dynamic')

    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def toJson(self):
        return jsonify_object(self)

    def serialize(self):
        return jsonify_object(self)

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    @property
    def created_day(self):
        return self.created_at.date()

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return str(s.dumps({'confirm': self.id}).decode())

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return str(s.dumps({'reset': self.id}).decode())

    def confirm_account(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password_hash = generate_password_hash(new_password)
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()
        if len(roles) <= 0:
            Role.insert_roles()
            roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                profession=fake.job(),
                city=fake.city(),
                country=fake.country(),
                zip=fake.postcode(),
                state=fake.state(),
                summary_text=fake.text(),
                password='password',
                confirmed=True,
                role=choice(roles),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


    def last_message(self, user_id):
        message = Message.query.order_by(Message.timestamp.desc()). \
            filter(or_(and_(Message.recipient_id == user_id, Message.user_id == self.id),
                       and_(Message.recipient_id == self.id, Message.user_id == user_id))).first()
        return message

    def history(self, user_id, unread=False):
        messages = Message.query.order_by(Message.timestamp.asc()). \
            filter(or_(and_(Message.recipient_id == user_id, Message.user_id == self.id),
                       and_(Message.recipient_id == self.id, Message.user_id == user_id))).all()
        return messages

    def new_messages(self, user_id=None):
        if not user_id:
            return Message.query.filter_by(recipient=self).filter(Message.read_at == None).distinct('user_id').count()
        else:
            return Message.query.filter_by(recipient=self).filter(Message.read_at == None).filter(
                Message.user_id == user_id).count()

    def add_notification(self, name, data, related_id=0, permanent=False):
        from app.email import send_email
        if not permanent:
            self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self, related_id=related_id)
        db.session.add(n)
        db.session.commit()
        n = Notification.query.get(n.id)
        kwargs = data
        kwargs['related'] = related_id
        get_queue().enqueue(
            send_email,
            recipient=self.email,
            subject='You Have a new notification on Mediville',
            template='account/email/notification',
            user=self.id,
            link=url_for('main.notifications', _external=True),
            notification=n.id,
            **kwargs
        )
        if not current_app.config['DEBUG']:
            ws_url = "https://www.mediville.com"
            path = 'sockets/socket.io'
        else:
            get_queue().empty()
            ws_url = "http://localhost:3000"
            path = "socket.io"
        sio = socketio.Client()
        sio.connect(ws_url + "?token={}".format(create_access_token(identity=current_user.id)), socketio_path=path)
        data = n.parsed()
        u = jsonify_object(data['user'])
        tu = jsonify_object(self)
        data['user'] = {key: u[key] for key in u.keys()
                        & {'first_name', 'id', 'email', 'socket_id'}}
        data['touser'] = {key: tu[key] for key in tu.keys()
                          & {'first_name', 'id', 'email', 'socket_id'}}
        sio.emit('new_notification', {'notification': data})
        return n

    def get_photo(self):
        photos = self.photos.all()
        if len(photos) > 0:
            return url_for('_uploads.uploaded_file', setname='images',
                           filename=photos[0].image_filename, _external=True)
        else:
            if self.gender == 'Female':
                return "https://1.semantic-ui.com/images/avatar/large/veronika.jpg"
            else:
                return "https://1.semantic-ui.com/images/avatar/large/jenny.jpg"

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


