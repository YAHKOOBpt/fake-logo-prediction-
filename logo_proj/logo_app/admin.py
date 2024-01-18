from django.contrib import admin
from .models import *
# Register your models here.

from django.utils.html import format_html


class LogoPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image', 'result')
    list_display_links = ('id', 'display_image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50px" height="50px" />'.format(obj.image.url))
        else:
            return "No Image"

    display_image.short_description = 'Image Preview'

# Check if LogoPredictionAdmin is not already registered before registering
if not admin.site.is_registered(LogoPrediction):
    admin.site.register(LogoPrediction, LogoPredictionAdmin)
