from django.contrib import admin
from django.utils.html import format_html
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'role_tags',
        'major',
        'minor',
        'picture_preview',
        'created_at',
    )
    search_fields = ('name', 'major', 'minor')
    list_filter = ('year', 'dev', 'des', 'pm', 'core', 'mentor')
    readonly_fields = ('created_at', 'updated_at', 'picture_preview_admin')
    ordering = ('name',)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "year", "major", "minor", "picture", "picture_preview_admin")
        }),
        ("Roles", {
            "fields": ("dev", "des", "pm", "core", "mentor"),
        }),
        ("Bio", {
            "fields": (
                "birthday", "home", "quote", "favorite_thing_1",
                "favorite_thing_2", "favorite_thing_3",
                "favorite_dartmouth_tradition", "fun_fact",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        })
    )

    # Small picture preview in list display
    def picture_preview(self, obj):
        if not obj.picture:
            return "-"
        return format_html(
            '<img src="{}" style="height:40px; width:40px; object-fit:cover; border-radius:6px;" />',
            obj.picture
        )
    picture_preview.short_description = "Photo"

    # Bigger preview in detail page
    def picture_preview_admin(self, obj):
        if not obj.picture:
            return "No image"
        return format_html(
            '<img src="{}" style="height:120px; border-radius:8px;" />',
            obj.picture
        )
    picture_preview_admin.short_description = "Preview"

    # Roles displayed cleanly in list display
    def role_tags(self, obj):
        roles = obj.get_roles()
        if not roles:
            return "-"
        return ", ".join(roles)
    role_tags.short_description = "Roles"
