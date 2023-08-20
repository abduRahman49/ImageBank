from rest_framework import filters


class StatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset