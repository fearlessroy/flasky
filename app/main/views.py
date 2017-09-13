# -*- encoding=utf-8 -*-
from datetime import datetime
from threading import Thread

from flask import render_template, session, redirect, url_for, flash, abort
from flask_mail import Message

from manage import app
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db, mail
from ..models import User
from ..decorators import admin_required, permission_required
from ..models import Permission
from flask_login import login_required, current_user


def send_anync_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_anync_email, args=[app, msg])
    # mail.send(msg)
    thr.start()
    return thr


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/test', methods=['GET', 'POST'])
def test():
    return '<h1>Hello World!</h1>'


@main.route('/admin')
@login_required
@admin_required
def for_amdins_only():
    return 'For administrators!'


@main.route('/moderator')
@login_required
@permission_required(Permission.FOLLOW)
def for_moderators_only():
    return "For comment moderators"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
