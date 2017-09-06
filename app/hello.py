# # -*- coding=utf-8 -*-
#
# import os
# from datetime import datetime
# from threading import Thread
# from flask import Flask, render_template, session, redirect, url_for, flash
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from flask_script import Manager, Shell
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'stay hungry stay foolish'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['MAIL_SERVER'] = 'smtp.126.com'  # smtp host
# app.config['MAIL_PORT'] = '25'  # port
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'w739709403@126.com'
# app.config['MAIL_PASSWORD'] = ''  # 授权码
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# # app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
# app.config['FLASKY_MAIL_SENDER'] = 'w739709403@126.com'
# app.config['FLASKY_ADMIN'] = '739709403@qq.com'
#
# db = SQLAlchemy(app)
# bootstrap = Bootstrap(app)
# manager = Manager(app)
# moment = Moment(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
# mail = Mail(app)
#
#
# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[DataRequired()])  # 确保提交的字段不为空
#     submit = SubmitField('Submit')
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Integer, unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#
# def make_sehll_context():
#     return dict(app=app, db=db, User=User, Role=Role)
#
#
# manager.add_command("shell", Shell(make_context=make_sehll_context))
#
#
# def send_anync_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_mail(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
#                   recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_anync_email, args=[app, msg])
#     # mail.send(msg)
#     thr.start()
#     return thr
#
#
# # @app.route('/sendmail')
# # def send_mail():
# #     msg = Message('主题', sender='w739709403@126.com', recipients=['739709403@qq.com'])
# #     msg.body = '文本 body'
# #     msg.html = '<b>HTML</b> body'
# #     mail.send(msg)
# #
# #     return '<h1>邮件发送成功</h1>'
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # return '<h1>Hello World!</h1>'
#
#     # user_agent = request.headers.get('User-Agent')  # 请求上下文 request和session
#     # return '<p>Your browser is %s</p>' % user_agent
#     # response = make_response('<h1>This document carries a cookie!</h1>')
#     # response.set_cookie('answer', '42')
#     # return response
#     # return redirect('http://baidu.com')
#
#     # form = NameForm()
#     # if form.validate_on_submit():
#     #     old_name = session.get('name')
#     #     if old_name and old_name != form.name.data:
#     #         flash('Looks like you have changed your name!')
#     #     session['name'] = form.name.data
#     #     return redirect(url_for('index'))
#     # return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))
#
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         user = User.query.filter_by(username=form.name.data).first()
#         if not user:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#             if app.config['FLASKY_ADMIN']:
#                 send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
#                            known=session.get('known', False))
#
#
# @app.route('/user/<name>')  # 静态路由
# def user(name):
#     # return '<h1>Hello %s!</h1>' % name
#     return render_template('user.html', name=name)
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
#
#
# if __name__ == "__main__":
#     # app.run(debug=True)
#     manager.run()
