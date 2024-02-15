from django.contrib import admin
from .models import User, BLToken, Profile


admin.site.register(User)
admin.site.register(BLToken)
admin.site.register(Profile)
# Register your models here.
