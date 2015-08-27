from django.contrib import admin

from robox.models import File


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    fields = ['barcode']


admin.site.register(File, FileAdmin)
