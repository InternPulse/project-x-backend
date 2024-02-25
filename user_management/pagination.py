from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "status": 200,
            "success": True,
            "message": f"User list",
            "errors": {},
            "data": data,
            'page_info': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
        })