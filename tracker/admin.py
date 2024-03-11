from django.contrib import admin

from .models import YoutubeFilterTracker


@admin.register(YoutubeFilterTracker)
class YoutubeFilterTrackerAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created_by',
        'privacy_level',
        'share_count',
        'user_rating',
    ]
    empty_value_display = "-empty-"
    search_fields = ["title"]
    readonly_fields = ['start_date', 'end_date', 'logs', 'channels', 'video_tags']
