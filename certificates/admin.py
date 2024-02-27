from django.contrib import admin

from .models import Certificate


# Register your models here.
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cohort', 'intern_name', 'stack', 'issue_date', 'created_at', 'updated_at')
    list_filter = ('cohort', 'issue_date', 'created_at', 'updated_at')
    search_fields = ('id', 'user', 'cohort', 'intern_name', 'stack')

admin.site.register(Certificate, CertificateAdmin)
