"""Performance management models."""
from django.db import models


class PerformanceReview(models.Model):
    """Stores structured performance review data for an employee."""

    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE, related_name="performance_reviews")
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    reviewer_name = models.CharField(max_length=120)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    overall_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-review_period_end", "employee__last_name"]
        indexes = [
            models.Index(fields=["employee", "review_period_end"]),
            models.Index(fields=["review_period_start", "review_period_end"]),
        ]

    def __str__(self) -> str:
        return f"Review {self.review_period_start} - {self.review_period_end} for {self.employee}"
