"""Project level URL configuration."""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from employees.api import EmployeeViewSet
from attendance.api import AttendanceRecordViewSet
from performance.api import PerformanceReviewViewSet

router = routers.DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"attendance", AttendanceRecordViewSet, basename="attendance")
router.register(r"performance", PerformanceReviewViewSet, basename="performance")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/reports/", include("reports.urls")),
]
