from django.contrib import admin
from .models import Post, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("author", "content", "created_at")
    can_delete = True


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ("member", "created_at")
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "content_preview", "content_type", "created_at", "like_count")
    list_filter = ("content_type", "created_at")
    search_fields = ("author__name", "content")
    readonly_fields = ("created_at", "updated_at", "like_count")
    inlines = [CommentInline, LikeInline]

    def author_name(self, obj):
        return obj.author.name
    author_name.short_description = "Author"

    def content_preview(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Preview"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "short_content", "created_at")
    search_fields = ("author__name", "content", "post__content")
    list_filter = ("created_at",)

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("member__name", "post__content")
    readonly_fields = ("created_at",)
