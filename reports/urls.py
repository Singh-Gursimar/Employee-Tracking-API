"""URL routes for reporting endpoints."""
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("headcount/", views.HeadcountReportView.as_view(), name="headcount"),
    path("attendance/", views.AttendanceReportView.as_view(), name="attendance"),
    path("performance/", views.PerformanceReportView.as_view(), name="performance"),
    path("employee/<int:employee_id>/", views.EmployeeSnapshotView.as_view(), name="employee-snapshot"),
]
