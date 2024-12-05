from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from ..models import Surveys
from .serializers import ListSurveysSerializer, SurveysSerializer


class SurveysViewSet(viewsets.ModelViewSet):
    serializer_class = SurveysSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = Surveys.objects.all()
    serializer_classes = {
        'list': ListSurveysSerializer,
    }
    filter_backends = [filters.SearchFilter,  filters.OrderingFilter, DjangoFilterBackend]
    ordering = ('-created_at')
    search_fields = ['id',]
    filterset_fields = { 'type', }
    lookup_field = 'slug'

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        # Obtener el usuario que está creando la encuesta
        user = self.request.user

        # Crear la instancia y guardar el usuario que realiza la creación
        instance = serializer.save(created_by=user)
        instance.save()

    def perform_update(self, serializer):
        # Obtenemos el usuario que está realizando la actualización
        user = self.request.user
        
        # Establecemos los campos de actualización
        instance = serializer.save()
        instance.update_at = timezone.now()  # Actualizamos la fecha de la última actualización
        instance.update_by = user  # Establecemos el usuario que realizó la actualización
        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
            
        user = self.request.user
        instance.status = 'CANCELED'
        instance.deleted_at=timezone.now()
        instance.deleted_by=user
        instance.save()

        # Retornar la respuesta exitosa sin eliminar físicamente
        return Response({'message': 'La encuenta se cancelo'}, status=status.HTTP_200_OK)
