# -*-coding=utf-8-*-
import os
from celery import Celery

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Permission, Post, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_sehll_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post, Comment=Comment)


manager.add_command("shell", Shell(make_context=make_sehll_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        # COV.stop()
        COV.save()
        print 'Coverage Summary:'
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print 'HTML version:file://%s/index.html' % covdir
        COV.erase()


'''
use:
python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade
'''


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User

    # 把数据库迁移到最新版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有用户都关注此用户
    User.add_self_follows()


# 从env文件中加在环境变量
# if os.path.exists('.env'):
#     print('Importing environment from .env...')
#     for line in open('.env'):
#         var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]

if __name__ == '__main__':
    manager.run()
