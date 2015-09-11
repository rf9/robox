from django.contrib import admin

from robox.models import File


# noinspection PyUnusedLocal
def reparse_file(modeladmin, request, queryset):
    for file in queryset.all():
        file.parse()


# noinspection PyUnusedLocal
def delete_stored_files(modeladmin, request, queryset):
    for obj in queryset:
        obj.file.delete()


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (File, 'file', 'format', 'barcode', 'upload_time')
    fields = ('barcode', 'file')
    list_filter = ('format', 'upload_time')
    search_fields = ['barcode']
    actions = [delete_stored_files, reparse_file]
