# import django_filters
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta

# from django_filters import rest_framework as filters
import pytz
from datetime import datetime, timezone
from django.db.models import Q

from django_filters import rest_framework as filters

from ..models import Surveys

# class SurveysFilter(django_filters.FilterSet):
#     start_date = filters.DateFilter(method='filter_start_date', label="Fecha de inicio")
#     end_date = filters.DateFilter(method='filter_end_date', label="Fecha final")

#     class Meta:
#         model = Surveys
#         fields = ['type', 'start_date', 'end_date']  # Define solo los campos del filtro, no necesariamente del modelo.


#     def filter_start_date(self, queryset, name, value):
#         # Asegura que el valor se convierta a zona horaria consciente
#         start_datetime = make_aware(datetime.combine(value, datetime.min.time()))
#         return queryset.filter(created_at__gte=start_datetime)

#     def filter_end_date(self, queryset, name, value):
#         # Asegura que se tome hasta el final del día
#         end_datetime = make_aware(datetime.combine(value, datetime.max.time()))
#         return queryset.filter(created_at__lte=end_datetime)


class SurveysFilter(filters.FilterSet):
    start_date = filters.DateFilter(method='filter_start_date', label="Fecha de inicio")
    end_date = filters.DateFilter(method='filter_end_date', label="Fecha final")

    category = filters.DateFilter(method='filter_category', label="Categoria")

    class Meta:
        model = Surveys
        fields = ['type', 'type_3', 'start_date', 'end_date', 'status', 'category']

    def filter_category(self, queryset, name, value):
        if value == 'PRODUCT':
            return queryset.filter(type_2='PRODUCT_QUALITY')
        elif value == 'SERVICE':
            return queryset.filter(type_2='BAD_SERVICE')
        
        return queryset.filter(~Q(type_2='PRODUCT_QUALITY'), ~Q(type_2='BAD_SERVICE'))
        

    def filter_start_date(self, queryset, name, value):
        # Convierte la fecha de inicio al inicio del día en la zona horaria local y luego a UTC
        local_tz = pytz.timezone('America/Mexico_City')
        start_datetime = local_tz.localize(datetime.combine(value, datetime.min.time())).astimezone(timezone.utc)
        return queryset.filter(created_at__gte=start_datetime)

    def filter_end_date(self, queryset, name, value):
        # Convierte la fecha final al final del día en la zona horaria local y luego a UTC
        local_tz = pytz.timezone('America/Mexico_City')
        end_datetime = local_tz.localize(datetime.combine(value, datetime.max.time())).astimezone(timezone.utc)
        return queryset.filter(created_at__lte=end_datetime)