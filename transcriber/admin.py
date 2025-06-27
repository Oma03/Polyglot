from django.contrib import admin
from .models import AudioUpload

# Register your models here.
class AudioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

admin.site.register(AudioUpload, AudioAdmin)
