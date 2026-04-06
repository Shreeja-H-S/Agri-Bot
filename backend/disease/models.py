from django.db import models
from users.models import User


class DiseasePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    image = models.ImageField(upload_to='disease_images/')
    result = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.result} ({self.created_at.date()})"
