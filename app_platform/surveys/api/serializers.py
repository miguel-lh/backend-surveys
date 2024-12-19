# encoding: utf-8

from rest_framework import serializers

from ..models import Surveys, SurveyComments


class CommentsSerialier(serializers.ModelSerializer):
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
    folio = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Surveys
        fields = ("folio", "slug", "created_at", "type", "description", "contact_name", "contact_phone", "status")
        read_only = (fields, )


class SurveysSerializer(serializers.ModelSerializer):
    folio = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Surveys
        exclude = ('id',)
        read_only = (
            "folio",
            "slug",
        )