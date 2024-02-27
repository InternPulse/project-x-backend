from django.contrib import admin

from .models import Certificate


# Register your models here.
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'cohort', 'title', 'description', 'image', 'issued_to', 'issue_date', 'created_at', 'updated_at')
    list_filter = ('issue_date', 'created_at', 'updated_at')
    search_fields = ('id', 'cohort', 'title', 'description', 'issued_to',)

admin.site.register(Certificate, CertificateAdmin)
