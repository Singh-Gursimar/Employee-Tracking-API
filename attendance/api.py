"""API endpoints for attendance records."""
import django_filters
from django.db.models import Count
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


class AttendanceRecordFilter(django_filters.FilterSet):
    date_after = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_before = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = AttendanceRecord
        fields = {
            "employee": ["exact"],
            "status": ["exact"],
        }


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related("employee")
    serializer_class = AttendanceRecordSerializer
    filterset_class = AttendanceRecordFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "employee__email",
        "notes",
    ]
    ordering_fields = ["date", "status", "employee__last_name"]
    ordering = ["-date"]

    @action(detail=False, methods=["get"], url_path="daily-summary")
    def daily_summary(self, request):
        """Provide aggregated attendance counts for the requested date (defaults to today)."""
        date_str = request.query_params.get("date")
        target_date = timezone.localdate()
        if date_str:
            try:
                target_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        records = self.queryset.filter(date=target_date)
        totals = records.values("status").order_by().annotate(count=Count("id"))
        summary = {item["status"]: item["count"] for item in totals}
        return Response({"date": target_date, "summary": summary})
