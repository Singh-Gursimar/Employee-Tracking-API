"""Attendance tracking models."""
from django.db import models


class AttendanceRecord(models.Model):
    """Represents a single day's attendance detail for an employee."""

    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        REMOTE = "remote", "Remote"
        SICK = "sick", "Sick"
        VACATION = "vacation", "Vacation"

    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices)
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date", "employee__last_name"]
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["employee", "date"]),
        ]

    def __str__(self) -> str:
        return f"{self.employee} {self.date} {self.status}"
