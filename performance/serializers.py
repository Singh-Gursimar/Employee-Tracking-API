"""Serializers for performance review resources."""
from rest_framework import serializers

from .models import PerformanceReview


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.__str__", read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_name",
            "review_period_start",
            "review_period_end",
            "reviewer_name",
            "rating",
            "strengths",
            "improvements",
            "goals",
            "overall_summary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "employee_name", "created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("review_period_start") or getattr(self.instance, "review_period_start", None)
        end = attrs.get("review_period_end") or getattr(self.instance, "review_period_end", None)
        if start and end and end < start:
            raise serializers.ValidationError("Review end date cannot be earlier than start date.")
        return attrs
