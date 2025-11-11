"""Serializers for attendance resources."""
from rest_framework import serializers

from .models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.__str__", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "status",
            "check_in_time",
            "check_out_time",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "employee_name", "created_at", "updated_at"]
