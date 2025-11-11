from django.contrib import admin

from .models import PerformanceReview


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "review_period_start",
        "review_period_end",
        "reviewer_name",
        "rating",
    )
    search_fields = ("employee__first_name", "employee__last_name", "reviewer_name")
    list_filter = ("review_period_end", "rating")
