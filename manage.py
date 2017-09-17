import os
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
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# @manager.command
# def init_database():
#     # db.drop_all()
#     db.create_all()
#     db.session.commit()
'''
use:
python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade
'''

if __name__ == '__main__':
    manager.run()
