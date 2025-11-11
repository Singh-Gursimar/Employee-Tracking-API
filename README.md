# Employee Tracking API

A RESTful API built with Django and Django REST Framework for managing employee records, attendance tracking, and performance reviews with automated HR analytics reporting.

## Features
- **CRUD Operations**: Full create, read, update, delete for employees, attendance records, and performance reviews
- **Advanced Filtering**: Search, filter, and sort across all endpoints with pagination
- **Automated Reporting**: Headcount summaries, attendance analytics, and performance insights
- **Normalized SQL Schema**: SQLite database with foreign keys, indexes, and constraints
- **Comprehensive Tests**: Full test coverage with pytest

## Quick Start

```powershell
# Activate virtual environment
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1

# Install dependencies (already done if you followed setup)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit:
- **API**: http://127.0.0.1:8000/api/
- **Admin**: http://127.0.0.1:8000/admin/
- **Reports**: http://127.0.0.1:8000/api/reports/

## API Endpoints

### Employees
- `GET/POST /api/employees/` - List or create employees
- `GET/PATCH/DELETE /api/employees/{id}/` - Retrieve, update, or delete employee
- `GET /api/employees/search/?q=term` - Search employees
- `GET /api/employees/{id}/insights/` - Employee analytics snapshot

### Attendance
- `GET/POST /api/attendance/` - List or create attendance records
- `GET/PATCH/DELETE /api/attendance/{id}/` - Manage attendance record
- `GET /api/attendance/daily-summary/?date=YYYY-MM-DD` - Daily attendance summary

### Performance Reviews
- `GET/POST /api/performance/` - List or create performance reviews
- `GET/PATCH/DELETE /api/performance/{id}/` - Manage performance review
- `GET /api/performance/top-performers/?limit=N` - Top performers by rating

### Reports & Analytics
- `GET /api/reports/headcount/` - Organization headcount by department and status
- `GET /api/reports/attendance/?days=N` - Attendance trends over period
- `GET /api/reports/performance/?days=N` - Performance insights over period
- `GET /api/reports/employee/{id}/` - Complete employee analytics snapshot

## Managing Data

### View Data

**Option 1: Django Admin (Web UI)**
```powershell
python manage.py runserver
# Visit http://127.0.0.1:8000/admin/
```

**Option 2: Command Line**
```powershell
python view_data.py
```

**Option 3: API Browser**
```powershell
# Visit http://127.0.0.1:8000/api/employees/
```

**Option 4: Python Shell**
```powershell
python manage.py shell
>>> from employees.models import Employee
>>> Employee.objects.all()
```

### Add Sample Data
```powershell
python add_sample_data.py
```

## Running Tests
```powershell
pytest
```

## Project Structure

```
Employee-Tracking-API/
├── config/              # Django settings and URLs
├── employees/           # Employee management app
│   ├── models.py       # Employee data model
│   ├── serializers.py  # REST API serializers
│   ├── api.py          # API viewsets and endpoints
│   ├── admin.py        # Django admin configuration
│   └── tests/          # Unit tests
├── attendance/          # Attendance tracking app
│   ├── models.py       # Attendance record model
│   ├── serializers.py  
│   ├── api.py          
│   └── tests/          
├── performance/         # Performance review app
│   ├── models.py       # Performance review model
│   ├── serializers.py  
│   ├── api.py          
│   └── tests/          
├── reports/            # Analytics and reporting
│   ├── services.py     # Business logic for reports
│   ├── views.py        # Report API endpoints
│   └── urls.py         # Report URL routing
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── pytest.ini          # Test configuration
├── add_sample_data.py  # Populate database with sample data
├── view_data.py        # View database contents
└── show_sql.py         # Display generated SQL queries
```

## Technology Stack
- **Framework**: Django 5.2+ with Django REST Framework
- **Database**: SQLite (easily swappable for PostgreSQL/MySQL)
- **Testing**: pytest with pytest-django
- **Filtering**: django-filter for advanced query capabilities

## Database Schema
- **employees_employee**: Core employee records with department, position, status
- **attendance_attendancerecord**: Daily attendance with check-in/out times
- **performance_performancereview**: Performance reviews with ratings and feedback
- Normalized design with foreign keys and indexes for optimal query performance