from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ["img", "preview_image", "order"]
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        size_attitude = obj.img.width / obj.img.height
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.img.url,
            width=200 * size_attitude,
            height=200,
            )
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]