"""API tests for performance endpoints."""
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from performance.models import PerformanceReview


class PerformanceAPITests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Katherine",
            last_name="Johnson",
            email="katherine@example.com",
            position="Analyst",
            department="Strategy",
            date_hired=date(2018, 4, 15),
        )
        PerformanceReview.objects.create(
            employee=self.employee,
            review_period_start=date(2023, 1, 1),
            review_period_end=date(2023, 6, 30),
            reviewer_name="Supervisor",
            rating=4.9,
        )

    def test_list_performance_reviews(self):
        url = reverse("performance-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["rating"], "4.90")

    def test_top_performers_endpoint(self):
        url = reverse("performance-top-performers")
        response = self.client.get(url, {"limit": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
