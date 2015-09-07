from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from .models import File, Item, Data


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        print("instance=%r, id=%r" % (instance, instance.pk))
        if instance.pk:
            url = reverse('admin:%s_%s_change' % (
                instance._meta.app_label, instance._meta.module_name),
                          args=[instance.pk])
            return mark_safe('<a href="%s">edit</a>' % url)
        return ''

    edit_link.allow_tags = True
    edit_link.short_description = "Edit link"


class DataInline(admin.TabularInline):
    model = Data
    fields = ['description', 'value']
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    model = Item
    fields = ['index']
    inlines = (DataInline,)


class ItemInline(admin.TabularInline):
    def edit_link(self, instance):
        print("instance=%r, id=%r" % (instance, instance.pk))
        if instance.pk:
            url = '/admin/garage/item/%s/' % instance.pk
            return mark_safe('<a href="%s">Edit item</a>' % url)
        return ''

    edit_link.allow_tags = True
    edit_link.short_description = "Edit link"
    model = Item
    readonly_fields = ['index', 'edit_link']
    fields = ['index', 'edit_link']
    extra = 0


class FileAdmin(admin.ModelAdmin):
    model = File
    fields = ['barcode', 'filename', 'upload_date']
    inlines = (ItemInline,)


admin.site.register(File, FileAdmin)
admin.site.register(Item, ItemAdmin)
