"""API tests for attendance endpoints."""
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from attendance.models import AttendanceRecord
from employees.models import Employee


class AttendanceAPITests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Grace",
            last_name="Hopper",
            email="grace@example.com",
            position="Manager",
            department="Operations",
            date_hired=date(2019, 6, 1),
        )
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="api_tester", password="pass1234")

    def test_create_attendance_record(self):
        url = reverse("attendance-list")
        payload = {
            "employee": self.employee.id,
            "date": "2024-02-01",
            "status": AttendanceRecord.Status.PRESENT,
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AttendanceRecord.objects.count(), 1)

    def test_daily_summary(self):
        AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2024, 2, 2),
            status=AttendanceRecord.Status.REMOTE,
        )
        url = reverse("attendance-daily-summary")
        response = self.client.get(url, {"date": "2024-02-02"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["summary"][AttendanceRecord.Status.REMOTE], 1)
