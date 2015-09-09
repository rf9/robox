from django.contrib import admin

from robox.models import File


def reparse_file(modeladmin, request, queryset):
    for file in queryset.all():
        file.parse()


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (File, 'file', 'format', 'barcode', 'upload_time')
    fields = ('barcode', 'file')
    list_filter = ('format', 'upload_time')
    search_fields = ['barcode']
    actions = [reparse_file]
