from django.contrib import admin
from django.utils.html import format_html

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "department",
        "position",
        "status",
        "has_user_account",
        "date_hired",
    )
    search_fields = ("first_name", "last_name", "email", "department", "position")
    list_filter = ("department", "status", "is_active")
    readonly_fields = ("created_at", "updated_at", "user_account_info")
    
    fieldsets = (
        ("Personal Information", {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ("Employment Details", {
            'fields': ('position', 'department', 'date_hired', 'status', 'is_active')
        }),
        ("User Account", {
            'fields': ('user', 'user_account_info'),
            'description': 'User account for employee portal login. Auto-created when employee is saved.'
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_user_account(self, obj):
        """Display if employee has a user account."""
        if obj.user:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    has_user_account.short_description = "Has Login"
    
    def user_account_info(self, obj):
        """Display user account credentials information."""
        if obj.user:
            return format_html(
                '<div style="background: #e8f5e9; padding: 10px; border-radius: 5px;">'
                '<strong>Username:</strong> {}<br>'
                '<strong>Email:</strong> {}<br>'
                '<strong>Active:</strong> {}<br>'
                '<em style="color: #666;">Employee can login at the main page (/) with this username.</em>'
                '</div>',
                obj.user.username,
                obj.user.email,
                "Yes" if obj.user.is_active else "No"
            )
        return format_html(
            '<div style="background: #fff3cd; padding: 10px; border-radius: 5px;">'
            '<strong>No user account yet.</strong><br>'
            '<em>A user account will be created automatically when you save this employee.</em>'
            '</div>'
        )
    user_account_info.short_description = "Login Account Details"
