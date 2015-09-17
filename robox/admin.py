from django.contrib import admin

from robox.models import DataFile, BinaryFile


# noinspection PyUnusedLocal
def reparse_file(modeladmin, request, queryset):
    for file in queryset.all():
        file.parse()


@admin.register(DataFile)
class FileAdmin(admin.ModelAdmin):
    list_display = (DataFile, 'binary_file', 'format', 'barcode', 'upload_time')
    fields = ('barcode', 'binary_file')
    list_filter = ('format', 'upload_time')
    search_fields = ['barcode']
    actions = [reparse_file]


@admin.register(BinaryFile)
class BinaryFileAdmin(admin.ModelAdmin):
    list_display = ['name']
