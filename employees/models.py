"""Data models for employee management."""
from django.db import models


class Employee(models.Model):
    """Stores core employee profile information."""

    class EmploymentStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        ON_LEAVE = "on_leave", "On Leave"
        TERMINATED = "terminated", "Terminated"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    date_hired = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["department", "status"])]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
