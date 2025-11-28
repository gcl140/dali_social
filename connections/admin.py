from django.contrib import admin
from .models import Connection
from django.utils.html import format_html

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        'from_member',
        'to_member',
        'colored_status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'from_member__name',
        'to_member__name',
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def colored_status(self, obj):
        color = {
            'pending': 'orange',
            'accepted': 'green',
            'rejected': 'red',
        }.get(obj.status, 'black')

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.capitalize()
        )

    colored_status.short_description = "Status"
