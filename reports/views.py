"""REST endpoints that expose reporting insights."""
from dataclasses import asdict

from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee

from . import services


class HeadcountReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        payload = services.headcount_summary()
        return Response(payload)


class AttendanceReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        days = request.query_params.get("days")
        days_arg = int(days) if days is not None and days.isdigit() else None
        summary = services.attendance_summary(days_arg)
        return Response(asdict(summary))


class PerformanceReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        days = request.query_params.get("days")
        days_arg = int(days) if days is not None and days.isdigit() else None
        summary = services.performance_summary(days_arg)
        return Response(asdict(summary))


class EmployeeSnapshotView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, employee_id: int):
        try:
            payload = services.employee_snapshot(employee_id)
        except Employee.DoesNotExist as exc:
            raise Http404 from exc
        return Response(payload)
