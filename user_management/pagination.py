from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Questionnaire
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()
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

class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    role = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role']


class QuestionnaireFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')

    class Meta:
        model = Questionnaire
        fields = ['first_name', 'last_name']