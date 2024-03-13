import json
import logging

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder

# Get an instance of a logger
logger = logging.getLogger(__name__)


channel_layer = get_channel_layer()


def send_update(user_id, **kwargs):
    group_name = f'user_{user_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'task_thread',
            'message': kwargs,
        },
    )


@shared_task
def channel_statistics_api_task(*args, **kwargs):
    """
    A Celery task to call the YouTube API and fetch channel statistics.
    """
    user_id = kwargs.get('user_id', None)
    channel_ids = kwargs.get('channel_ids', [])
    total_channels = len(channel_ids)

    try:
        # Send initial update
        send_update(
            user_id,
            status='Processing',
            channels='Initializing...',
            progress='0%',
        )

        for index, channel_id in enumerate(channel_ids, start=1):
            # Update progress every iteration
            progress_percentage = (index / total_channels) * 100
            send_update(
                user_id,
                status='Processing',
                channels=f'{index}/{total_channels}',
                progress=f'{progress_percentage:.2f}%',
            )
            import time

            # Simulate work being done
            time.sleep(1)

        # Send completion message
        send_update(user_id, status='Completed')

        # Log the task arguments
        logging.info(f"Task arguments: {json.dumps(kwargs, cls=DjangoJSONEncoder)}")
        return None

    except Exception as e:
        # Inform the user about any errors
        error_message = f'Error: {str(e)}'
        send_update(user_id, status=error_message)
        logging.error(f'Error in channel statistics api task: {error_message}')
    finally:
        # Close the WebSocket connection
        send_update(user_id, status='CLOSE_CONNECTION')
