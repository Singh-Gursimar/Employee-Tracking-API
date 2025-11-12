"""
Data models for employee management.

Models in Django are like blueprints for database tables.
Each class becomes a table, each attribute becomes a column!
"""
from django.db import models
from django.contrib.auth.models import User  # Django's built-in user model for login/auth


class Employee(models.Model):
    """
    Stores core employee profile information.
    
    This is the main employee table - it has all the info about an employee
    like their name, position, department, etc.
    
    We link it to Django's User model so employees can login!
    """

    class EmploymentStatus(models.TextChoices):
        """
        Enum for employee status options.
        
        TextChoices is a nice way to define dropdown options.
        First value is what's stored in DB, second is what users see.
        """
        ACTIVE = "active", "Active"  # Currently working
        ON_LEAVE = "on_leave", "On Leave"  # Temporarily not working
        TERMINATED = "terminated", "Terminated"  # No longer with company

    # This creates a one-to-one link with Django's User model
    # One employee = one user account for logging in
    # null=True and blank=True means it's optional (for now - signals will fill it)
    # related_name lets us do user.employee_profile to get the employee from a user
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,  # If user is deleted, delete employee too
        null=True, 
        blank=True, 
        related_name="employee_profile"
    )
    
    # Basic info fields
    first_name = models.CharField(max_length=100)  # CharField = text field with max length
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # EmailField validates it's a real email format
    position = models.CharField(max_length=120)  # Job title
    department = models.CharField(max_length=120)  # Which department they work in
    date_hired = models.DateField()  # When they joined (DateField = date only, no time)
    
    # Status field using our choices from above
    status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,  # Dropdown options
        default=EmploymentStatus.ACTIVE,  # New employees are active by default
    )
    
    # Whether the employee account is active (different from employment status!)
    is_active = models.BooleanField(default=True)  # Can they login to portal?
    
    # Timestamps - Django automatically fills these in
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when created
    updated_at = models.DateTimeField(auto_now=True)  # Updated every time we save

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["department", "status"])]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
