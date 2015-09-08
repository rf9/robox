from django.contrib import admin
from django.contrib.admin.filters import BooleanFieldListFilter

from robox.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (File, 'file', 'format', 'barcode', 'upload_time')
    fields = ('barcode', 'file')
    list_filter = ('format', 'upload_time')
    search_fields = ['barcode']
