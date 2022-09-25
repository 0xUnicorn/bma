from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "gallery",
        "uuid",
        "created",
        "updated",
        "title",
        "original",
        "tags"
    ]
    list_filter = ["tags"]
