import django_filters
from django_filters import rest_framework as filters


from ..models import Surveys

class SurveysFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr='gte', label="Fecha de inicio")
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr='lte', label="Fecha final")

    class Meta:
        model = Surveys
        fields = ['type', 'start_date', 'end_date']  # Define solo los campos del filtro, no necesariamente del modelo.
