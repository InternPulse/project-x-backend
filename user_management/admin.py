from django.contrib import admin

from .models import BLToken, Profile, User

admin.site.register(User)
admin.site.register(BLToken)
admin.site.register(Profile)
