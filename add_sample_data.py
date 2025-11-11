"""Populate the database with sample employee, attendance, and performance data."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date, timedelta
from employees.models import Employee
from attendance.models import AttendanceRecord
from performance.models import PerformanceReview


print("="*80)
print("ADDING SAMPLE DATA")
print("="*80)

# Add more employees
print("\n📊 Adding employees...")
employees_data = [
    {
        "first_name": "Alan",
        "last_name": "Turing",
        "email": "alan.turing@example.com",
        "position": "Principal Engineer",
        "department": "Engineering",
        "date_hired": date(2018, 3, 15),
    },
    {
        "first_name": "Margaret",
        "last_name": "Hamilton",
        "email": "margaret.hamilton@example.com",
        "position": "Software Architect",
        "department": "Engineering",
        "date_hired": date(2019, 7, 1),
    },
    {
        "first_name": "John",
        "last_name": "von Neumann",
        "email": "john.neumann@example.com",
        "position": "Chief Scientist",
        "department": "Research",
        "date_hired": date(2017, 1, 10),
    },
]

created_employees = []
for emp_data in employees_data:
    emp, created = Employee.objects.get_or_create(
        email=emp_data["email"],
        defaults=emp_data
    )
    if created:
        created_employees.append(emp)
        print(f"✓ Created: {emp.first_name} {emp.last_name}")
    else:
        print(f"- Already exists: {emp.first_name} {emp.last_name}")

# Add attendance records for new employees
print("\n📅 Adding attendance records...")
today = date.today()
attendance_count = 0

for emp in created_employees:
    for i in range(7):
        record_date = today - timedelta(days=i)
        # Vary the status
        if i % 5 == 0:
            status = AttendanceRecord.Status.REMOTE
        elif i % 7 == 0:
            status = AttendanceRecord.Status.SICK
        else:
            status = AttendanceRecord.Status.PRESENT
        
        _, created = AttendanceRecord.objects.get_or_create(
            employee=emp,
            date=record_date,
            defaults={
                "status": status,
                "check_in_time": "09:00" if status != AttendanceRecord.Status.SICK else None,
                "check_out_time": "17:30" if status == AttendanceRecord.Status.PRESENT else None,
            }
        )
        if created:
            attendance_count += 1

print(f"✓ Added {attendance_count} attendance records")

# Add performance reviews
print("\n⭐ Adding performance reviews...")
review_data = [
    {
        "employee_email": "alan.turing@example.com",
        "review_period_start": date(2024, 1, 1),
        "review_period_end": date(2024, 6, 30),
        "reviewer_name": "Director of Engineering",
        "rating": 4.95,
        "strengths": "Revolutionary problem-solving approach, exceptional technical depth",
        "improvements": "Could delegate more routine tasks",
        "goals": "Lead flagship cryptography project",
    },
    {
        "employee_email": "margaret.hamilton@example.com",
        "review_period_start": date(2024, 1, 1),
        "review_period_end": date(2024, 6, 30),
        "reviewer_name": "VP of Engineering",
        "rating": 4.85,
        "strengths": "Meticulous attention to detail, excellent system design",
        "improvements": "Balance perfection with delivery timelines",
        "goals": "Establish software quality standards",
    },
    {
        "employee_email": "john.neumann@example.com",
        "review_period_start": date(2024, 1, 1),
        "review_period_end": date(2024, 6, 30),
        "reviewer_name": "Chief Technology Officer",
        "rating": 5.00,
        "strengths": "Visionary thinking, cross-disciplinary expertise",
        "improvements": "Simplify communication for broader audiences",
        "goals": "Drive research roadmap for next 3 years",
    },
]

review_count = 0
for review_info in review_data:
    email = review_info.pop("employee_email")
    try:
        employee = Employee.objects.get(email=email)
        _, created = PerformanceReview.objects.get_or_create(
            employee=employee,
            review_period_start=review_info["review_period_start"],
            review_period_end=review_info["review_period_end"],
            defaults=review_info
        )
        if created:
            review_count += 1
            print(f"✓ Created review for {employee.first_name} {employee.last_name}")
    except Employee.DoesNotExist:
        pass

print(f"✓ Added {review_count} performance reviews")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Employees: {Employee.objects.count()}")
print(f"Attendance Records: {AttendanceRecord.objects.count()}")
print(f"Performance Reviews: {PerformanceReview.objects.count()}")
print("\n✅ Sample data added!")
print("Run 'python view_data.py' to view all data")
print("="*80)
