from rest_framework import serializers
from .models import AudioUpload


class AudioUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioUpload
        fields = ['audio', 'created_at', 'transcribed_text', 'audio_id']