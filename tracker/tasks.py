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
        # Send to as message current_loop of /total_channels channels

        for index, channel_id in enumerate(channel_ids, start=1):
            # Update progress every iteration
            task_info = {
                'status': 'PROGRESS',
                'channeels': f'{index}/{total_channels}',
                'progress': f'{(index / total_channels) * 100:.2f}%',
            }
            send_update(user_id, **task_info)

            # Simulate work being done
            import time

            time.sleep(1)

        # Log the task arguments
        logging.info(f"Task arguments: {json.dumps(kwargs, cls=DjangoJSONEncoder)}")
        return None

    except Exception as e:
        # Inform the user about any errors
        send_update(user_id, status=f'Error: {str(e)}')
        print(f'Error in channel statistics api task: {str(e)}')
    finally:
        # Close the WebSocket connection
        send_update(user_id, status='CLOSE_CONNECTION')
