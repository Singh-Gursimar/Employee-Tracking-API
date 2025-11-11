"""API endpoints for employee resources."""
from django.db.models import Avg, Count, Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from attendance.models import AttendanceRecord
from performance.models import PerformanceReview

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ["first_name", "last_name", "email", "department", "position"]
    ordering_fields = ["first_name", "last_name", "date_hired", "department"]
    ordering = ["last_name", "first_name"]
    filterset_fields = {
        "department": ["exact"],
        "status": ["exact"],
        "is_active": ["exact"],
        "date_hired": ["gte", "lte"],
    }

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """Provide text search endpoint for quick employee lookups."""
        term = request.query_params.get("q")
        if not term:
            return Response({"detail": "Provide a q query parameter."}, status=400)
        queryset = self.queryset.filter(
            Q(first_name__icontains=term)
            | Q(last_name__icontains=term)
            | Q(email__icontains=term)
            | Q(department__icontains=term)
        )[:25]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="insights")
    def insights(self, request, pk=None):
        """Return key HR signals for the specified employee."""
        employee = self.get_object()
        attendance_stats = employee.attendance_records.aggregate(
            total_days=Count("id"),
            present_days=Count("id", filter=Q(status=AttendanceRecord.Status.PRESENT)),
            absent_days=Count("id", filter=Q(status=AttendanceRecord.Status.ABSENT)),
        )
        reviews = employee.performance_reviews.aggregate(
            average_rating=Avg("rating"),
            review_count=Count("id"),
        )
        return Response(
            {
                "employee": EmployeeSerializer(employee).data,
                "attendance": attendance_stats,
                "performance": {
                    "average_rating": round(reviews["average_rating"], 2) if reviews["average_rating"] else None,
                    "review_count": reviews["review_count"],
                },
            }
        )
