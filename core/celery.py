# yapf: disable
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

app = Celery('platfo', namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def mins_to_seconds(mins):
    return mins * 60


tasks = {
    # 'celery_execute_drivers_near_bound_task': {
    #     'task': 'etl.tasks.execute_drivers_near_bound_task',
    #     'schedule': crontab(hour=1, minute=0),
    # },
    # 'celery_update_client_service_level_from_concurrency': {
    #     'task': 'concurrency.tasks.update_client_service_level_from_concurrency',
    #     'schedule': mins_to_seconds(5),
    # },
}

# app.conf.beat_schedule = tasks

# app.conf.task_routes = (
#     [
#         ('utilities.tasks.send_sms_task', {'queue': 'sms'}),
#         ('utilities.tasks.send_plain_text_sms_task', {'queue': 'sms'}),
#         ('utilities.tasks.send_otp_sms_task', {'queue': 'sms'}),
#         ('etl.tasks.*', {'queue': 'etl'}),
#         ('*', {'queue': 'default'}),
#     ],
# )
