from django.conf import settings
from django.db import models


class UserRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="media_ratings",
    )

    media_id = models.IntegerField()
    media_type = models.CharField(max_length=20)

    media_title = models.CharField(max_length=255, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )

    text = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "media_id", "media_type")

    def __str__(self):
        return f"{self.user} - {self.media_title} - {self.rating}"
