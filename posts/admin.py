from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "updated_at", "created_at"]
    list_filter = ["updated_at", "created_at"]
    list_display_links = ["updated_at", "created_at"]
    list_editable = ["title"]
    search_fields = ["title", "content"]

admin.site.register(Post, PostAdmin)
