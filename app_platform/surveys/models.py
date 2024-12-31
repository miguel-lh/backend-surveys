# encoding: utf-8
from uuid import uuid4

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords

from app_platform.users.models import User
from .constants import *

class Surveys(models.Model):
    slug = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name=_('uuid'))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_surveys')
    update_at = models.DateTimeField(_('Ultima actualizacion'), null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_surveys')
    deleted_at = models.DateTimeField(_('Eliminado'), null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_surveys')

    
    description = models.TextField(_('Descripcion'), null=True, blank=True)
    type = models.CharField(_('Tipo'), choices=TYPE_SURVEYS, )
    status = models.CharField(_('Tipo'), choices=STATUS_SURVEYS, default='PENDING', null=True, blank=True)
    
    
    # Tipos y sub tipos solo aplican de acuerdo al tipo 
    type_2 = models.CharField(_('Tipo 2'), choices=TYPE_2_SURVEYS, null=True, blank=True)
    type_3 = models.CharField(_('Tipo 3'), choices=TYPE_3_SURVEYS, null=True, blank=True)

    # Datos del contacto solo aplican para el tipo de sugerencia
    contact_name = models.CharField(_('Nombre del contacto'), max_length=2000, null=True, blank=True)
    contact_phone = models.CharField(_('Telefono del contacto'), max_length=2000, null=True, blank=True)
    contact_email = models.CharField(_('Email del contacto'), max_length=2000, null=True, blank=True)
    
    # Ranking solo aplica para el typo felicitacion
    ranking = models.IntegerField(_('Ranking de sugerencia'), null=True, blank=True)

    is_removed = models.BooleanField(_('Eliminado'), default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f'# {self.id}'
    
    class Meta:
        verbose_name='Encuenta'
        verbose_name_plural='Encuestas'


class SurveyComments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    slug = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name=_('uuid'))
    
    # update_at = models.DateTimeField(_('Ultima actualizacion'), null=True, blank=True)
    # update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_surveys')
    # deleted_at = models.DateTimeField(_('Eliminado'), null=True, blank=True)
    # deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_surveys')

    survey = models.ForeignKey(Surveys, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField()

    
    is_removed = models.BooleanField(_('Eliminado'), default=False)

    def __str__(self):
        return f"Comment of {self.survey.folio} by {self.user}"

