# Employee Tracking API with Employee Portal 🏢

A full-featured employee management system with:
- **RESTful API** for managing employees, attendance, and performance reviews
- **Employee Self-Service Portal** where employees can login and manage their own attendance
- **Automatic Account Creation** for new employees
- **HR Analytics & Reporting**

## ✨ Main Features

### For Employees (Employee Portal)
- 🔐 **Login at Main Page** - http://127.0.0.1:8000/
- 📊 **Personal Dashboard** - View your attendance stats and history
- ✅ **Self-Service Attendance** - Mark yourself present/absent/remote/sick/vacation
- 📝 **Absence Reasons** - Required to provide reasons for absences
- 📈 **Track Your Stats** - See your attendance rate and trends

### For Admins (REST API)
- **CRUD Operations**: Full create, read, update, delete for employees, attendance records, and performance reviews
- **Advanced Filtering**: Search, filter, and sort across all endpoints with pagination
- **Automated Reporting**: Headcount summaries, attendance analytics, and performance insights
- **Normalized SQL Schema**: SQLite database with foreign keys, indexes, and constraints
- **Comprehensive Tests**: Full test coverage with pytest
- **Auto User Accounts**: New employees automatically get login credentials

## 🚀 Quick Start

### Step 1: Install & Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Add sample data and create employee accounts
python add_sample_data.py
python setup_employee_portal.py
```

### Step 2: Start the Server
```powershell
python manage.py runserver
```

### Step 3: Access the System

**Employee Portal (Main Page):**
- 🏠 **Login**: http://127.0.0.1:8000/
- Use credentials: 
  - Username: `margaret.hamilton` (or `grace`, `katherine`, `ada`)
  - Password: `employee123`

**Admin & API:**
- 👨‍💼 **Admin Panel**: http://127.0.0.1:8000/admin/ (create superuser first)
- 🔌 **API Endpoints**: http://127.0.0.1:8000/api/
- 📊 **Reports**: http://127.0.0.1:8000/api/reports/

## 🎯 Employee Portal Usage

### For Employees: How to Mark Attendance

1. **Login** at http://127.0.0.1:8000/
2. You'll see your **dashboard** with:
   - Your attendance statistics
   - Recent attendance history
   - Form to mark today's attendance
3. **Select Status**:
   - **Present** - Working on-site
   - **Remote** - Working from home  
   - **Absent** - Not working
   - **Sick** - Sick leave
   - **Vacation** - Vacation time
4. **Add Check-in/out times** (optional)
5. **Provide Reason** (required for Absent/Sick/Vacation)
6. Click **Submit Attendance**

### For Admins: Adding New Employees

**New employees automatically get login accounts!**

#### Method 1: Django Admin (Easiest)
```powershell
# Create superuser if you haven't
python manage.py createsuperuser

# Start server and go to admin
python manage.py runserver
# Visit http://127.0.0.1:8000/admin/
```

1. Click **Employees** → **Add Employee**
2. Fill in employee details (name, email, position, etc.)
3. Click **Save**
4. ✨ **User account automatically created!**
5. Share credentials with employee:
   - Username: `[from their email]`
   - Password: `employee123`
   - Portal: http://127.0.0.1:8000/

#### Method 2: Python Code
```python
from employees.models import Employee
from datetime import date

# Create employee
employee = Employee.objects.create(
    first_name="Jane",
    last_name="Doe",
    email="jane.doe@company.com",
    position="Software Engineer",
    department="Engineering",
    date_hired=date.today(),
    status="active"
)

# User account is AUTO-CREATED!
# Username: jane.doe
# Password: employee123
```

#### Method 3: Bulk Import
```powershell
# Edit and run this script for multiple employees
python add_sample_data.py
```

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

## 🔐 How Auto Account Creation Works

When you add a new employee, the system **automatically**:

1. Creates a Django User account
2. Generates username from email (e.g., `john.doe@company.com` → `john.doe`)
3. Sets default password: `employee123`
4. Links the user to the employee record
5. Employee can immediately login!

**Implementation**: Uses Django signals in `employees/signals.py` that trigger on employee creation.

## 🛠️ Management Commands

```powershell
# Create user accounts for all employees without one
python manage.py create_employee_users

# With custom password
python manage.py create_employee_users --default-password "YourPassword"

# Test auto-account creation
python test_auto_account.py

# View all employee credentials
python setup_employee_portal.py
```

## 🔧 Troubleshooting

### Employee Can't Login?
1. Check if they have a user account: Admin → Employees → look for "Has Login" ✓
2. Username is their email prefix (before @)
3. Default password is `employee123`

### No Account Auto-Created?
1. Check `employees/apps.py` has the `ready()` method
2. Restart Django server
3. Or manually run: `python setup_employee_portal.py`

### Reset Employee Password?
```powershell
python manage.py shell
```
```python
from django.contrib.auth.models import User
user = User.objects.get(username='john.doe')
user.set_password('newpassword123')
user.save()
```

## 📋 Project URLs

| URL | Purpose |
|-----|---------|
| `/` | Employee login page (main page) |
| `/dashboard/` | Employee dashboard (after login) |
| `/logout/` | Logout |
| `/mark-attendance/` | Submit attendance (POST) |
| `/admin/` | Django admin panel |
| `/api/` | REST API root |
| `/api/employees/` | Employee API endpoints |
| `/api/attendance/` | Attendance API endpoints |
| `/api/performance/` | Performance API endpoints |
| `/api/reports/` | Analytics & reports |

## 💻 Technology Stack
- **Backend**: Django 5.2+ with Django REST Framework
- **Database**: SQLite (easily swappable for PostgreSQL/MySQL)
- **Authentication**: Django's built-in auth system with sessions
- **Frontend**: Server-side rendered templates (HTML/CSS)
- **Testing**: pytest with pytest-django
- **Filtering**: django-filter for advanced queries
- **Signals**: Auto user account creation

## 🗄️ Database Schema
- **employees_employee**: Core employee records with department, position, status (linked to User)
- **attendance_attendancerecord**: Daily attendance with check-in/out times and notes
- **performance_performancereview**: Performance reviews with ratings and feedback
- **auth_user**: Django's user table for authentication
- Normalized design with foreign keys and indexes for optimal query performance

## 🎨 Key Files Explained

### Employee Portal
- `config/templates/` - Login and dashboard HTML templates
- `employees/views.py` - Login, logout, dashboard logic
- `employees/forms.py` - Login and attendance forms
- `employees/signals.py` - Auto-creates user accounts for new employees

### REST API
- `employees/api.py` - Employee API endpoints
- `attendance/api.py` - Attendance API endpoints
- `performance/api.py` - Performance API endpoints
- `reports/views.py` - Analytics and reporting endpoints

### Models
- `employees/models.py` - Employee model (linked to Django User)
- `attendance/models.py` - Attendance record model
- `performance/models.py` - Performance review model

## 🚀 Future Enhancements

Ideas for extending the system:
- [ ] Password change functionality for employees
- [ ] Email notifications when accounts are created
- [ ] Manager approval workflow for time off requests
- [ ] Mobile-responsive design improvements
- [ ] Export attendance to PDF/Excel
- [ ] Forgot password / password reset
- [ ] Two-factor authentication
- [ ] Employee profile pictures
- [ ] Leave balance tracking
- [ ] Shift scheduling

## 📝 Default Login Credentials

After running `setup_employee_portal.py`, sample employees can login with:

- **Username**: `margaret.hamilton`, `grace`, `katherine`, `ada`
- **Password**: `employee123` (for all employees)
- **Portal**: http://127.0.0.1:8000/

⚠️ **Important**: Employees should change their password after first login!

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Improve the UI/UX
- Add more comprehensive tests
- Optimize database queries
- Add better error handling

## 📄 License

This project is for educational purposes.