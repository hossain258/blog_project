from django.contrib import admin
from .models import Content, Tag

class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "text")


admin.site.register(Content, ContentAdmin)
admin.site.register(Tag)
