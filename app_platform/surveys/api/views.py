# encoding: utf-8
import os
import pandas as pd


from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status as response_status

from ..models import Surveys, SurveyComments
from .serializers import ListSurveysSerializer, SurveysSerializer, CommentsSerialier, CommentsOnSerialier
from .filters import SurveysFilter


class SurveyCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerialier
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = SurveyComments.objects.all()
    lookup_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise MethodNotAllowed(request.method)
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Obtener el usuario que está creando la encuesta
        user = self.request.user

        # Crear la instancia y guardar el usuario que realiza la creación
        instance = serializer.save(user=user)
        instance.save()


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
    search_fields = ['id', 'contact_name', 'contact_phone', 'contact_email',]
    filterset_class = SurveysFilter
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create':  # Permitir acceso a usuarios no autenticados en `POST`
            return [AllowAny()]
        return [IsAuthenticated()]
    

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        # Obtener el usuario que está creando la encuesta
        user = self.request.user if self.request.user.is_authenticated else None
        user = self.request.user if self.request.user else None

        
        serializer.save(created_by=user)

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

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def comments(self, request, slug=None):
        instance =  self.get_object()

        comments = instance.comments.all().order_by('-id')
        serializer = CommentsOnSerialier(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, slug=None):
        # Obtener el objeto correspondiente al slug
        instance = self.get_object()

        # Validar que el atributo 'status' esté presente en el cuerpo de la solicitud
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {"error": "El campo 'status' es obligatorio."},
                status=response_status.HTTP_400_BAD_REQUEST,
            )

        # Actualizar el atributo `status`
        instance.status = new_status

        if new_status == 'CANCELED':
            instance.date_status_to_cancelled=timezone.now()
        elif new_status == 'FINISHED':
            instance.date_status_to_finalized=timezone.now()


        instance.save()

        return Response(
            {"message": "Estatus actualizado correctamente.", "status": instance.status},
            status=response_status.HTTP_200_OK,
        )

    @action(detail=True, methods=['patch'], url_path='update-route')
    def update_route(self, request, slug=None):
        # Obtener el objeto correspondiente al slug
        instance = self.get_object()

        # Validar que el atributo 'status' esté presente en el cuerpo de la solicitud
        new_route = request.data.get('route')

        user = self.request.user

        # Actualizar el atributo `status`
        instance.route = new_route
        instance.update_at = timezone.now()  # Actualizamos la fecha de la última actualización
        instance.update_by = user  # Establecemos el usuario que realizó la actualización
        instance.save()


        return Response(
            {"message": "Ruta actualizado correctamente.", "route": instance.route},
            status=response_status.HTTP_200_OK,
        )


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export(self, request, slug=None):
        # Filtrar por rango de fechas (start_date y end_date como query params)
        search = request.query_params.get('search', None)
        type = request.query_params.get('type', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        
        filters = {
            'id__icontains': search,
            'type__exact': type,
            'created_at__gte': start_date,
            'created_at__lte': end_date
        }

        qfilters = {k: v for k, v in filters.items() if v is not None}


        # Ruta del archivo
        output_dir = str(settings.OUTPUT_FILES)
        dir_output_file = os.path.join(output_dir, 'encuestas.xlsx')

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        results = Surveys.objects.filter(**qfilters)

        # Definir nombres personalizados de columnas
        custom_column_names = {
            'folio': "FOLIO",
            'slug': "SLUG",
            'created_at': 'FECHA DE CREACIÓN',
            'type': 'TIPO',
            'description': 'DESCRIPCIÓN',
            'name': 'NOMBRE',
            'phone': 'CELULAR',
            'email': 'CORREO',
            'status': 'ESTATUS',
        }

        # Convertir el queryset en una lista de diccionarios directamente
        serialized_data = ListSurveysSerializer(results, many=True).data


        # Convertir los datos serializados a un DataFrame de pandas
        df = pd.DataFrame(serialized_data).rename(columns=custom_column_names)

        # Exportar los datos a un archivo Excel
        df.to_excel(dir_output_file, index=False)

        # Verificar que el archivo se ha creado correctamente
        if os.path.exists(dir_output_file):
            # Abrir el archivo sin usar el bloque 'with' para que no se cierre automáticamente
            file_handle = open(dir_output_file, 'rb')
            response = FileResponse(file_handle, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="encuestas.xlsx"'
            return response
        else:
            return Response({"error": "El archivo no pudo ser creado."}, status=400)
