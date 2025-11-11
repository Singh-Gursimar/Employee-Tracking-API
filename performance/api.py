"""API endpoints for performance reviews."""
import django_filters
from django.db.models import Avg, Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer


class PerformanceReviewFilter(django_filters.FilterSet):
    period_start_after = django_filters.DateFilter(field_name="review_period_start", lookup_expr="gte")
    period_end_before = django_filters.DateFilter(field_name="review_period_end", lookup_expr="lte")
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")

    class Meta:
        model = PerformanceReview
        fields = {
            "employee": ["exact"],
            "reviewer_name": ["icontains"],
        }


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.select_related("employee")
    serializer_class = PerformanceReviewSerializer
    filterset_class = PerformanceReviewFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "reviewer_name",
        "overall_summary",
    ]
    ordering_fields = [
        "review_period_start",
        "review_period_end",
        "rating",
        "employee__last_name",
    ]
    ordering = ["-review_period_end"]

    @action(detail=False, methods=["get"], url_path="top-performers")
    def top_performers(self, request):
        """Return the top N employees ranked by average rating."""
        top_n = request.query_params.get("limit", "5")
        try:
            limit = max(1, min(int(top_n), 50))
        except ValueError:
            return Response({"detail": "limit must be an integer."}, status=400)
        aggregates = (
            self.queryset.values("employee", "employee__first_name", "employee__last_name")
            .annotate(avg_rating=Avg("rating"), review_count=Count("id"))
            .order_by("-avg_rating", "-review_count")[:limit]
        )
        results = [
            {
                "employee_id": item["employee"],
                "employee_name": f"{item['employee__first_name']} {item['employee__last_name']}",
                "average_rating": round(item["avg_rating"], 2) if item["avg_rating"] is not None else None,
                "review_count": item["review_count"],
            }
            for item in aggregates
        ]
        return Response({"results": results, "limit": limit})
