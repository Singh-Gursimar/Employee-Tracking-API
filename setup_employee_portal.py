#!/usr/bin/env python
"""
Setup employee portal with sample data and user accounts.

This script creates login accounts for all employees so they can
access the employee portal at http://127.0.0.1:8000/

Run this after adding employees to give them login credentials!
"""
import os
import sys
import django

# Setup Django environment - needed when running Django code outside of manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from employees.models import Employee
from attendance.models import AttendanceRecord
from datetime import date, timedelta, time

def setup_employee_portal():
    """Setup employee portal with user accounts."""
    print("=" * 60)
    print("Employee Portal Setup")
    print("=" * 60)
    
    # First, check if there are any employees in the database
    employees = Employee.objects.all()
    if not employees.exists():
        print("\n⚠️  No employees found in the database.")
        print("Please run 'python add_sample_data.py' first to create sample employees.")
        return
    
    print(f"\n✓ Found {employees.count()} employees in the database")
    
    # Find employees who don't have user accounts yet
    # user__isnull=True means "where user field is NULL/empty"
    employees_without_users = Employee.objects.filter(user__isnull=True)
    
    if employees_without_users.exists():
        print(f"\n📝 Creating user accounts for {employees_without_users.count()} employees...")
        default_password = 'employee123'  # Same password for everyone (for now - they should change it!)
        
        # Loop through each employee and create their account
        for employee in employees_without_users:
            # Create username from email (everything before the @)
            # Example: "john.doe@company.com" → "john.doe"
            username = employee.email.split('@')[0]
            
            # Check if username already exists (maybe from another employee)
            # If it does, add a number: john.doe1, john.doe2, etc.
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Create the user account using Django's built-in method
            # create_user automatically hashes the password for security
            user = User.objects.create_user(
                username=username,
                email=employee.email,
                password=default_password,
                first_name=employee.first_name,
                last_name=employee.last_name,
            )
            
            # Link the user to the employee (creates the relationship)
            employee.user = user
            employee.save()
            
            # Print the credentials so admin can share them with the employee
            print(f"  ✓ Created: {employee.first_name} {employee.last_name}")
            print(f"    Username: {username}")
            print(f"    Password: {default_password}")
            print()
    else:
        print("\n✓ All employees already have user accounts!")
    
    # Display all employee credentials for reference
    print("\n" + "=" * 60)
    print("Employee Login Credentials")
    print("=" * 60)
    
    # Get all employees who have user accounts, sorted by last name
    for employee in Employee.objects.filter(user__isnull=False).order_by('last_name'):
        print(f"\n{employee.first_name} {employee.last_name}")
        print(f"  Position: {employee.position}")
        print(f"  Username: {employee.user.username}")
        print(f"  Email: {employee.email}")
    
    # Success message with instructions
    print("\n" + "=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print("\nTo access the employee portal:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Open your browser to: http://127.0.0.1:8000/")
    print("3. Login with any employee's username and password: employee123")
    print("\n⚠️  IMPORTANT: Employees should change their passwords after first login!")
    print()

# This runs when you execute the script directly (not when importing it)
if __name__ == '__main__':
    setup_employee_portal()
