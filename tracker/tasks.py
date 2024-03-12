import json
import logging

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder

# Get an instance of a logger
logger = logging.getLogger(__name__)


channel_layer = get_channel_layer()


def send_update(message, user_id):
    group_name = f'user_{user_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'task_thread',
            'message': message,
        },
    )


@shared_task
def channel_statistics_api_task(*args, **kwargs):
    user_id = kwargs.get('user_id')
    """
    A Celery task to call the YouTube API and fetch channel statistics.
    """
    try:
        # Inform the user that the task has started
        send_update('Task started.', user_id)

        # Simulate some task progress
        for i in range(5):
            # Update progress every iteration
            send_update({'progress': i}, user_id)
            # Simulate work being done
            import time

            time.sleep(1)

        # Get the result or status of the Celery task
        result = 'Task completed!'
        # You can also use tracker.result to get the AsyncResult object and extract more information if needed
        # For example, result = tracker.result.result

        # Inform the user that the task has completed
        send_update(result, user_id)

        # Log the task arguments
        logging.info(f"Task arguments: {json.dumps(kwargs, cls=DjangoJSONEncoder)}")
        return None

    except Exception as e:
        # Inform the user about any errors
        send_update(f'Error: {str(e)}', user_id)
        print(f'Error in channel statistics api task: {str(e)}')
    finally:
        # Close the WebSocket connection
        send_update('CLOSE_CONNECTION', user_id)
