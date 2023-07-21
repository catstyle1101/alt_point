from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProjectViewPagination(PageNumberPagination):
    """
    Pagination to views in project.
    """

    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                'limit': self.get_page_size(self.request),
                'page': self.get_page_number(self.request, self),
                'total': self.page.paginator.count,
                'results': data,
            }
        )
