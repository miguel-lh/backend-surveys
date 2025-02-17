# encoding: utf-8
import pytz
from rest_framework import serializers

from ..models import Surveys, SurveyComments



class CommentsSerialier(serializers.ModelSerializer):

    survey = serializers.SlugRelatedField(
        queryset=Surveys.objects.all(),  # Consulta para obtener la instancia de Survey.
        slug_field='folio'              # Campo único que se usará para la relación.
    )
    class Meta:
        model = SurveyComments
        exclude = ()
        read_only = (
            "id",
            "slug",
        )


class CommentsOnSerialier(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()


    class Meta:
        model = SurveyComments
        exclude = ('survey',)

    def get_user_name(self, obj):
        if obj.user:  # Verifica si el usuario está asignado
            return obj.user.name
        return "Usuario no asignado"


class ListSurveysSerializer(serializers.ModelSerializer):
    folio = serializers.CharField(read_only=True)
    created_at = serializers.SerializerMethodField()
    route = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Surveys
        fields = ("folio", "slug", "created_at", "route", "type", "description", "contact_name", "contact_phone", "contact_email", "status", "date_status_to_cancelled", "date_status_to_finalized")
        read_only = (fields, )

    def get_route(self, obj):
        if obj.route:
            return obj.route
        
        return 'No asignado'
    
    
    def get_created_at(self, obj):
        mexico_tz = pytz.timezone('America/Mexico_City')
        fecha_mexico = obj.created_at.astimezone(mexico_tz)

        return fecha_mexico.strftime('%Y-%m-%d %H:%M')

    def get_type(self, obj):
        if obj.type:
            return obj.get_type_display()
        
    # def get_status(self, obj):
    #     if obj.status:
    #         return obj.get_status_display()


class SurveyFolioRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Campo relacionado personalizado que permite recibir el folio de la encuesta
    y buscar la instancia correspondiente.
    """
    def to_internal_value(self, data):
        # Intentamos obtener la encuesta por su atributo 'folio'
        try:
            return self.get_queryset().get(folio=data)
        except Surveys.DoesNotExist:
            raise serializers.ValidationError(f'No se encontró una encuesta con el folio "{data}".')
        
class SurveysSerializer(serializers.ModelSerializer):
    folio = serializers.CharField(read_only=True)
    
    class Meta:
        model = Surveys
        exclude = ('id',)
        read_only = (
            "folio",
            "slug",
        )