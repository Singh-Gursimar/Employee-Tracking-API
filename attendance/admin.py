from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "date", "status", "check_in_time", "check_out_time")
    search_fields = ("employee__first_name", "employee__last_name", "notes")
    list_filter = ("status", "date")
