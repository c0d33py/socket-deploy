import json
import logging

from celery import shared_task
from django.core.serializers.json import DjangoJSONEncoder


@shared_task
def channel_statistics_api_task(*args, **kwargs):
    """
    A Celery task to call the YouTube API and fetch channel statistics.
    """
    # Log the task arguments
    logging.info(f"Task arguments: {json.dumps(kwargs, cls=DjangoJSONEncoder)}")
    return None
