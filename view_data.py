"""View all data in the Employee Tracking database."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from employees.models import Employee
from attendance.models import AttendanceRecord
from performance.models import PerformanceReview


print("="*80)
print("EMPLOYEE TRACKING DATABASE")
print("="*80)

# Employees
print("\n📊 EMPLOYEES")
print("-"*80)
employees = Employee.objects.all()
for emp in employees:
    print(f"ID: {emp.id:2} | {emp.first_name} {emp.last_name:20} | "
          f"{emp.department:15} | {emp.position}")
print(f"\nTotal: {employees.count()} employees")

# Attendance Records
print("\n📅 ATTENDANCE RECORDS (Last 10)")
print("-"*80)
attendance = AttendanceRecord.objects.select_related('employee').all()[:10]
for record in attendance:
    print(f"{record.date} | {record.employee.first_name} {record.employee.last_name:20} | "
          f"{record.status}")
print(f"\nTotal: {AttendanceRecord.objects.count()} attendance records")

# Performance Reviews
print("\n⭐ PERFORMANCE REVIEWS")
print("-"*80)
reviews = PerformanceReview.objects.select_related('employee').all()
for review in reviews:
    print(f"{review.employee.first_name} {review.employee.last_name:20} | "
          f"Rating: {review.rating} | Period: {review.review_period_start} to {review.review_period_end}")
print(f"\nTotal: {reviews.count()} performance reviews")

print("\n" + "="*80)
