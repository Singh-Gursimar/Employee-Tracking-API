"""
Attendance tracking models.

This keeps track of who's at work, who's absent, etc.
Each record represents one day for one employee.
"""
from django.db import models


class AttendanceRecord(models.Model):
    """
    Represents a single day's attendance detail for an employee.
    
    This is like a daily check-in record. Each employee can have one
    attendance record per day (enforced by unique_together below).
    """

    class Status(models.TextChoices):
        """
        Different types of attendance status.
        
        These are the options employees can choose when marking attendance.
        """
        PRESENT = "present", "Present"  # At the office
        ABSENT = "absent", "Absent"  # Not working (needs reason!)
        REMOTE = "remote", "Remote"  # Working from home
        SICK = "sick", "Sick"  # Sick day (needs reason!)
        VACATION = "vacation", "Vacation"  # Planned time off (needs reason!)

    # Foreign key links this record to an employee
    # ForeignKey = many-to-one relationship (many attendance records for one employee)
    # on_delete=CASCADE means if employee is deleted, delete all their attendance too
    # related_name lets us do employee.attendance_records.all() to get all their records
    employee = models.ForeignKey(
        "employees.Employee",  # String reference to avoid circular imports
        on_delete=models.CASCADE, 
        related_name="attendance_records"
    )
    
    date = models.DateField()  # Which day is this for?
    
    status = models.CharField(
        max_length=20, 
        choices=Status.choices  # Dropdown options from above
    )
    
    # Optional fields - not everyone tracks exact times
    check_in_time = models.TimeField(blank=True, null=True)  # What time they arrived
    check_out_time = models.TimeField(blank=True, null=True)  # What time they left
    
    # TextField for longer text (no max length, unlike CharField)
    # This is where employees write why they're absent/sick/on vacation
    notes = models.TextField(blank=True)  # blank=True means it's optional in forms
    
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class defines extra options for the model.
        
        This is where we set things like database constraints, ordering, etc.
        """
        # unique_together means we can't have duplicate (employee, date) pairs
        # So one employee can only have ONE attendance record per day!
        unique_together = ("employee", "date")
        
        # Default ordering when we query - most recent first, then alphabetically by last name
        ordering = ["-date", "employee__last_name"]  # - means descending
        
        # Database indexes speed up queries on these fields
        # Like an index in a book - makes lookups faster!
        indexes = [
            models.Index(fields=["date", "status"]),  # Fast lookups by date and status
            models.Index(fields=["employee", "date"]),  # Fast lookups for specific employee's dates
        ]

    def __str__(self) -> str:
        """
        String representation of the object.
        
        This is what shows up when you print() the object or see it in admin.
        Example: "John Doe 2025-11-11 present"
        """
        return f"{self.employee} {self.date} {self.status}"
