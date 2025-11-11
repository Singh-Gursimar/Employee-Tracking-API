"""Domain services for analytics and reporting."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from django.conf import settings
from django.db.models import Avg, Count, Max, Q
from django.utils import timezone

from attendance.models import AttendanceRecord
from employees.models import Employee
from performance.models import PerformanceReview


@dataclass
class AttendanceSummary:
    period_start: date
    period_end: date
    totals: dict[str, int]
    attendance_rate: float


@dataclass
class PerformanceSummary:
    period_start: date
    period_end: date
    average_rating: float | None
    review_count: int
    top_performers: list[dict[str, Any]]


def _now_date() -> date:
    return timezone.localdate()


def _reporting_config() -> dict[str, Any]:
    return getattr(settings, "REPORTING_CONFIG", {})


def headcount_summary() -> dict[str, Any]:
    """Compute current headcount distribution across the organization."""
    employees = Employee.objects.all()
    totals = employees.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(status=Employee.EmploymentStatus.ACTIVE)),
        on_leave=Count("id", filter=Q(status=Employee.EmploymentStatus.ON_LEAVE)),
        terminated=Count("id", filter=Q(status=Employee.EmploymentStatus.TERMINATED)),
    )
    by_department = (
        employees.values("department")
        .annotate(
            total=Count("id"),
            active=Count("id", filter=Q(status=Employee.EmploymentStatus.ACTIVE)),
        )
        .order_by("department")
    )
    return {
        "totals": totals,
        "by_department": list(by_department),
    }


def attendance_summary(days: int | None = None) -> AttendanceSummary:
    """Aggregate attendance mix and rate over a configurable period."""
    config = _reporting_config()
    window = days or config.get("RECENT_PERIOD_DAYS", 30)
    period_end = _now_date()
    period_start = period_end - timedelta(days=window)
    records = AttendanceRecord.objects.filter(date__range=(period_start, period_end))
    totals: dict[str, int] = defaultdict(int)
    for item in records.values("status").annotate(count=Count("id")):
        totals[item["status"]] = item["count"]
    present_days = totals.get(AttendanceRecord.Status.PRESENT, 0)
    worked_days = sum(totals.values())
    attendance_rate = (present_days / worked_days) if worked_days else 0.0
    return AttendanceSummary(
        period_start=period_start,
        period_end=period_end,
        totals=dict(totals),
        attendance_rate=round(attendance_rate, 3),
    )


def performance_summary(days: int | None = None) -> PerformanceSummary:
    """Produce aggregate performance insights across the organization."""
    config = _reporting_config()
    window = days or config.get("RECENT_PERIOD_DAYS", 30)
    period_end = _now_date()
    period_start = period_end - timedelta(days=window)
    reviews = PerformanceReview.objects.filter(review_period_end__range=(period_start, period_end))
    aggregates = reviews.aggregate(avg_rating=Avg("rating"), review_count=Count("id"))
    threshold = config.get("PERFORMANCE_RATING_THRESHOLDS", {}).get("excellent", 4.5)
    top_performers = (
        reviews.values("employee", "employee__first_name", "employee__last_name")
        .annotate(avg_rating=Avg("rating"), reviews=Count("id"))
        .filter(avg_rating__gte=threshold)
        .order_by("-avg_rating")
    )
    return PerformanceSummary(
        period_start=period_start,
        period_end=period_end,
        average_rating=(round(aggregates["avg_rating"], 2) if aggregates["avg_rating"] is not None else None),
        review_count=aggregates["review_count"],
        top_performers=[
            {
                "employee_id": item["employee"],
                "employee_name": f"{item['employee__first_name']} {item['employee__last_name']}",
                "average_rating": round(item["avg_rating"], 2),
                "review_count": item["reviews"],
            }
            for item in top_performers
        ],
    )


def employee_snapshot(employee_id: int) -> dict[str, Any]:
    """Combine HR signals for a specific employee to simulate analytics pipelines."""
    employee = Employee.objects.get(pk=employee_id)
    attendance = AttendanceRecord.objects.filter(employee=employee).aggregate(
        total_days=Count("id"),
        present_days=Count("id", filter=Q(status=AttendanceRecord.Status.PRESENT)),
        absent_days=Count("id", filter=Q(status=AttendanceRecord.Status.ABSENT)),
    )
    reviews = PerformanceReview.objects.filter(employee=employee)
    review_stats = reviews.aggregate(
        average_rating=Avg("rating"),
        review_count=Count("id"),
        last_review_end=Max("review_period_end"),
    )
    return {
        "employee": {
            "id": employee.id,
            "name": str(employee),
            "department": employee.department,
            "position": employee.position,
            "status": employee.status,
        },
        "attendance": attendance,
        "performance": {
            "average_rating": round(review_stats["average_rating"], 2) if review_stats["average_rating"] else None,
            "review_count": review_stats["review_count"],
            "last_review_end": review_stats["last_review_end"],
        },
    }
