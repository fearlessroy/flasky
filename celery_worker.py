from app import create_app_with_celery, celery
import os

app1 = create_app_with_celery(os.getenv('FLASK_CONFIG') or 'default')
app1.app_context().push()
