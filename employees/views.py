"""
Employee portal views for self-service attendance management.

These are the views (think of them as "pages") that employees see when they login.
We're using function-based views here (not class-based) because they're easier to understand!
"""
from django.contrib.auth import authenticate, login, logout  # Django's built-in auth functions
from django.contrib.auth.decorators import login_required  # Decorator to protect views from non-logged-in users
from django.contrib import messages  # For showing success/error messages to users
from django.shortcuts import render, redirect  # render = show template, redirect = go to different URL
from django.utils import timezone  # For getting current date/time
from django.db.models import Count, Q  # Q lets us do complex database queries (like OR conditions)
from datetime import datetime, timedelta

from employees.models import Employee
from attendance.models import AttendanceRecord
from .forms import EmployeeLoginForm, AttendanceMarkForm


def employee_login(request):
    """
    Handle employee login.
    
    This view shows the login form and processes login attempts.
    If user is already logged in, redirect them to dashboard.
    """
    # If user is already logged in, send them to the dashboard
    if request.user.is_authenticated:
        try:
            # Check if they have an employee profile (not all users are employees!)
            employee = request.user.employee_profile
            if employee.is_active:
                return redirect('employee_dashboard')
        except Employee.DoesNotExist:
            # User exists but isn't an employee - this shouldn't happen but just in case
            pass
    
    # Check if this is a form submission (POST) or just viewing the page (GET)
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():  # Check if form data is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with the provided credentials
            user = authenticate(request, username=username, password=password)
            
            if user is not None:  # Authentication successful!
                # Make sure this user is actually an employee and is active
                try:
                    employee = user.employee_profile
                    if employee.is_active:
                        # Log them in! This creates a session
                        login(request, user)
                        messages.success(request, f'Welcome back, {employee.first_name}!')
                        return redirect('employee_dashboard')
                    else:
                        # Employee exists but their account is deactivated
                        messages.error(request, 'Your employee account is inactive.')
                except Employee.DoesNotExist:
                    # User exists but has no employee profile
                    messages.error(request, 'No employee profile found for this account.')
            else:
                # Authentication failed - wrong username or password
                messages.error(request, 'Invalid username or password.')
    else:
        # GET request - just show the empty form
        form = EmployeeLoginForm()
    
    # Render the login template with the form
    return render(request, 'login.html', {'form': form})


def employee_logout(request):
    """
    Handle employee logout.
    
    Super simple - just log them out and redirect to login page.
    """
    logout(request)  # This destroys the session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('employee_login')


@login_required(login_url='employee_login')  # This decorator means you MUST be logged in to access this view
def employee_dashboard(request):
    """
    Display employee dashboard with attendance information.
    
    This is the main page employees see after login - shows their stats and
    lets them mark attendance.
    """
    # Get the employee profile for the logged-in user
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        # Shouldn't happen since we check in login, but safety first!
        messages.error(request, 'No employee profile found for your account.')
        return redirect('employee_login')
    
    # Get recent attendance records (last 30 days, limited to 15 most recent)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_records = AttendanceRecord.objects.filter(
        employee=employee,
        date__gte=thirty_days_ago  # gte = greater than or equal to
    ).order_by('-date')[:15]  # Order by date descending, take first 15
    
    # Calculate statistics for the employee
    total_records = AttendanceRecord.objects.filter(employee=employee)
    stats = {
        'total_days': total_records.count(),
        # Count days where status is 'present' OR 'remote' (both count as working)
        'present_days': total_records.filter(
            Q(status='present') | Q(status='remote')  # | means OR in Django queries
        ).count(),
        'absent_days': total_records.filter(status='absent').count(),
        'attendance_rate': 0  # We'll calculate this next
    }
    
    # Calculate attendance rate as a percentage
    if stats['total_days'] > 0:
        stats['attendance_rate'] = round(
            (stats['present_days'] / stats['total_days']) * 100, 1
        )
    
    # Create a blank form for marking attendance
    form = AttendanceMarkForm()
    
    # Pack everything into a context dictionary to send to the template
    context = {
        'employee': employee,
        'recent_records': recent_records,
        'stats': stats,
        'form': form,
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='employee_login')
def mark_attendance(request):
    """
    Handle attendance marking by employee.
    
    This is a POST-only view (no GET) - it processes the attendance form
    from the dashboard and creates/updates an attendance record.
    """
    # Only accept POST requests (form submissions)
    if request.method != 'POST':
        return redirect('employee_dashboard')
    
    # Get the employee profile
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No employee profile found.')
        return redirect('employee_login')
    
    # Create form with the submitted data
    form = AttendanceMarkForm(request.POST)
    
    if form.is_valid():
        # Get today's date
        today = timezone.now().date()
        
        # Extract cleaned (validated) data from form
        status = form.cleaned_data['status']
        check_in_time = form.cleaned_data.get('check_in_time')
        check_out_time = form.cleaned_data.get('check_out_time')
        notes = form.cleaned_data.get('notes', '')
        
        # Business rule: If marking absent/sick/vacation, they MUST provide a reason!
        if status in ['absent', 'sick', 'vacation'] and not notes.strip():
            messages.error(request, 'Please provide a reason for your absence.')
            return redirect('employee_dashboard')
        
        # Create or update attendance record for today
        # update_or_create is cool - it tries to find existing record, if found updates it, if not creates new
        attendance, created = AttendanceRecord.objects.update_or_create(
            employee=employee,
            date=today,
            defaults={  # These are the fields to set/update
                'status': status,
                'check_in_time': check_in_time,
                'check_out_time': check_out_time,
                'notes': notes,
            }
        )
        
        # Show appropriate success message
        if created:
            messages.success(request, f'Attendance marked as {attendance.get_status_display()} for today.')
        else:
            messages.success(request, f'Attendance updated to {attendance.get_status_display()} for today.')
    else:
        # Form validation failed - show errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    
    # Always redirect back to dashboard after processing
    return redirect('employee_dashboard')
