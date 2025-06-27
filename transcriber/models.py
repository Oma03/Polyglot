from django.db import models
from authentication.models import User
import uuid

# Create your models here.


class AudioUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio/')
    created_at = models.DateTimeField(auto_now_add=True)
    transcribed_text = models.CharField(max_length=1000000000, null=True)
    audio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.email