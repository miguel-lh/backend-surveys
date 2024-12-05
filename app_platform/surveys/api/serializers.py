# encoding: utf-8

from rest_framework import serializers

from ..models import Surveys

class ListSurveysSerializer(serializers.ModelSerializer):
    folio = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Surveys
        fields = ("folio", "slug", "created_at", "type", "description", "name", "phone", "status")
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