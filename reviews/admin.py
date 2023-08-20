from django.contrib import admin
from django.utils.html import format_html
from .models import *


class ImageWithTitleAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{url}" style="max-width:200px; max-height:200px"/>'
                           .format(url=obj.image.url))

    list_display = ['title', 'image_tag', ]


class ImageWithNameAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{url}" style="max-width:200px; max-height:200px"/>'
                           .format(url=obj.image.url))

    list_display = ['name', 'image_tag', ]


admin.site.register(News, ImageWithTitleAdmin)
admin.site.register(Image)
admin.site.register(Cultural)
admin.site.register(Gallery)
admin.site.register(Championship)
admin.site.register(Result)
admin.site.register(Game, ImageWithNameAdmin)
admin.site.register(Dormitories, ImageWithNameAdmin)
admin.site.register(Gym, ImageWithNameAdmin)
admin.site.register(Competition)
admin.site.register(Survey)
