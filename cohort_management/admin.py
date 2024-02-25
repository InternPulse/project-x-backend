# cohort_management/admin.py
from django.contrib import admin

from .models import Cohort, InternProfile


class CohortAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'rules', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'rules',)

admin.site.register(Cohort, CohortAdmin)


class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cohort', 'role', 'certificate_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'cohort__title', 'role')

admin.site.register(InternProfile, InternProfileAdmin)
