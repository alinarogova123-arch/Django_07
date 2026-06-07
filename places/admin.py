from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline
from adminsortable2.admin import SortableStackedInline
from adminsortable2.admin import SortableAdminBase

from .models import Place, Image


class ImageInline(SortableStackedInline):
    model = Image
    extra = 1
    fields = ["img", "preview_image", "order"]
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        size_attitude = obj.img.width / obj.img.height
        return format_html('<img src="{url}" style="max-width: {width}px; max-height: {height}px;" />',
            url = obj.img.url,
            width=400,
            height=200,
        )

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['place']

