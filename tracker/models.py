from django.contrib.auth.models import User
from django.db import models


class YoutubeFilterTracker(models.Model):
    """
    User youtube report proceesing filter tracker to store the filter data.
    """

    class RatingOption(models.IntegerChoices):
        ONE_STAR = 1, '1 Star'
        TWO_STARS = 2, '2 Stars'
        THREE_STARS = 3, '3 Stars'
        FOUR_STARS = 4, '4 Stars'
        FIVE_STARS = 5, '5 Stars'

    class PrivacyLevel(models.TextChoices):
        PUBLIC = 'Public'
        PRIVATE = 'Private'

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.PositiveBigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)
    channels = models.TextField()
    video_tags = models.TextField(blank=True)
    logs = models.JSONField(verbose_name='JSON data set', null=True)
    # Additional attributes
    share_count = models.PositiveIntegerField(default=0)
    user_rating = models.PositiveIntegerField(
        choices=RatingOption.choices, null=True, blank=True
    )
    privacy_level = models.CharField(
        max_length=7, choices=PrivacyLevel.choices, default='Private'
    )

    @classmethod
    def create_history_entry(
        cls,
        json_logs,
        created_by,
        category_id=None,
        channels=None,
        privacy_level='Private',
    ):
        return cls.objects.create(
            created_by=created_by,
            category=category_id,
            logs=json_logs,
            channels=channels,
            privacy_level=privacy_level,
        )

    class Meta:
        verbose_name_plural = 'Youtube Filter Tracker'
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title

    def increment_share_count(self):
        """
        Increment the share count for the video.
        """
        self.share_count += 1
        self.save()

    def set_user_rating(self, rating):
        """
        Set the user rating for the video.
        """
        if 1 <= rating <= 5:
            self.user_rating = rating
            self.save()

    # def get_average_rating(self):
    #     """
    #     Get the average user rating for the video.
    #     """
    #     return self.user_rating.aggregate(Avg('user_rating'))['user_rating__avg']

    def reset_user_rating(self):
        """
        Reset the user rating for the video.
        """
        self.user_rating = None
        self.save()
