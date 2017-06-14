from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .views import retrieve_articles

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="retrieve_articles",
    ignore_result=True
)
def task_retrieve_articles():
    """
    Saves latest image from Flickr
    """
    retrieve_articles()