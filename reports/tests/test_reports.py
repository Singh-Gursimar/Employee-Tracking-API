"""Integration tests for reporting endpoints."""
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from attendance.models import AttendanceRecord
from employees.models import Employee
from performance.models import PerformanceReview


class ReportsAPITests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Dorothy",
            last_name="Vaughan",
            email="dorothy@example.com",
            position="Lead",
            department="Engineering",
            date_hired=date(2017, 5, 20),
        )
        AttendanceRecord.objects.create(
            employee=self.employee,
            date=date.today(),
            status=AttendanceRecord.Status.PRESENT,
        )
        PerformanceReview.objects.create(
            employee=self.employee,
            review_period_start=date(2023, 7, 1),
            review_period_end=date(2023, 12, 31),
            reviewer_name="Manager",
            rating=4.8,
        )

    def test_headcount_report(self):
        url = reverse("reports:headcount")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["totals"]["total"], 1)

    def test_employee_snapshot(self):
        url = reverse("reports:employee-snapshot", kwargs={"employee_id": self.employee.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["employee"]["id"], self.employee.id)
