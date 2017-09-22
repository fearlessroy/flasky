from flask import Flask
from celery import Celery
import random


def make_celery(app):
    celery = Celery(app.import_name, broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')
    # celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)

# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )

celery = make_celery(app)


@celery.task
def add_together(a, b):
    res = a + b
    print 'adfafadfdas'
    return res


@app.route('/test-celery')
def test_celery():
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    res = add_together.delay(a, b).get()
    return 'Create new task {} + {} = {}'.format(a, b, res)



