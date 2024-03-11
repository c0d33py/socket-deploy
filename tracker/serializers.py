from rest_framework import serializers

from .models import YoutubeFilterTracker


class YoutubeFilterTrackerSerializer(serializers.ModelSerializer):
    """
    Youtube filter tracker serializer.
    """

    class Meta:
        model = YoutubeFilterTracker
        fields = '__all__'
        read_only_fields = [
            'logs',
            'share_count',
            'created_by',
        ]
