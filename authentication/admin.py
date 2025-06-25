from django.contrib import admin
from.models import User, Token

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'verified')


class TokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token')


admin.site.register(User, UserAdmin)
admin.site.register(Token, TokenAdmin)