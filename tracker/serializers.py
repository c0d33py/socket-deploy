from datetime import datetime, timezone

from rest_framework import serializers

from .models import YoutubeFilterTracker


class YoutubeFilterTrackerSerializer(serializers.ModelSerializer):
    """
    Youtube filter tracker serializer.
    """

    title = serializers.CharField(required=False)
    date_range = serializers.CharField(
        required=True, write_only=True, allow_blank=False
    )

    class Meta:
        model = YoutubeFilterTracker
        fields = '__all__'
        read_only_fields = [
            'logs',
            'share_count',
            'created_by',
            'start_date',
            'end_date',
        ]

    def get_date_range_string(self, range_stamp: str):
        start_date, end_date = range_stamp.split(' - ')

        # Corrected format for day/month/year, hour:minute AM/PM
        dt_object = datetime.strptime(start_date, '%d/%m/%Y, %I:%M %p')
        dt_object2 = datetime.strptime(end_date, '%d/%m/%Y, %I:%M %p')

        # Add timezone information (assuming UTC for this example)
        parsed_utc = dt_object.replace(tzinfo=timezone.utc)
        parsed_utc2 = dt_object2.replace(tzinfo=timezone.utc)

        return parsed_utc, parsed_utc2

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        date_range = internal_data.pop('date_range', '')

        parsed_utc, parsed_utc2 = self.get_date_range_string(date_range)

        internal_data['start_date'] = parsed_utc
        internal_data['end_date'] = parsed_utc2

        return internal_data
