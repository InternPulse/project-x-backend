# cohort_management/admin.py
from django.contrib import admin

from .models import Cohort, InternProfile

admin.site.register(Cohort)
admin.site.register(InternProfile)
