"""API tests for employee endpoints."""
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from attendance.models import AttendanceRecord
from employees.models import Employee
from performance.models import PerformanceReview


class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
            position="Engineer",
            department="R&D",
            date_hired=date(2020, 1, 1),
        )
        AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2024, 1, 2),
            status=AttendanceRecord.Status.PRESENT,
        )
        PerformanceReview.objects.create(
            employee=self.employee,
            review_period_start=date(2023, 1, 1),
            review_period_end=date(2023, 12, 31),
            reviewer_name="Alan Turing",
            rating=4.7,
        )

    def test_list_employees(self):
        url = reverse("employee-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["email"], "ada@example.com")

    def test_employee_insights_endpoint(self):
        url = reverse("employee-insights", kwargs={"pk": self.employee.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attendance", response.data)
        self.assertIn("performance", response.data)
        self.assertEqual(response.data["performance"]["review_count"], 1)
