# encoding: utf-8
from uuid import uuid4

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.db.models import Max
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

    folio = models.CharField(_('Folio'), max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(_('Descripcion'), null=True, blank=True)
    type = models.CharField(_('Tipo'), choices=TYPE_SURVEYS, )
    status = models.CharField(_('Tipo'), choices=STATUS_SURVEYS, default='PENDING', null=True, blank=True)
    
    date_status_to_cancelled  = models.DateTimeField(_('Fecha de cancelacion'), null=True, blank=True)
    date_status_to_finalized  = models.DateTimeField(_('Fecha de finalizado'), null=True, blank=True)


    # Tipos y sub tipos solo aplican de acuerdo al tipo 
    type_2 = models.CharField(_('Tipo 2'), choices=TYPE_2_SURVEYS, null=True, blank=True)
    type_3 = models.CharField(_('Tipo 3'), choices=TYPE_3_SURVEYS, null=True, blank=True)

    route = models.CharField(_('Ruta'), null=True, blank=True)

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
    

    def save(self, *args, **kwargs):
        if not self.folio:
            # Define prefijos para cada tipo
            prefix_map = {
                'COMPLAINT': 'Q',
                'SUGGESTION': 'S',
                'CONGRATULATION': 'F'
            }
            
            # Obtén el prefijo correspondiente al tipo
            prefix = prefix_map.get(self.type, '')
            if prefix:
                # Encuentra el máximo consecutivo existente para el tipo
                max_folio = Surveys.objects.filter(type=self.type).aggregate(Max('folio'))
                max_folio_value = max_folio['folio__max']
                
                # Extraer el número del folio anterior
                if max_folio_value:
                    last_consecutive = int(max_folio_value.lstrip(prefix)) + 1 
                else:
                    last_consecutive = 0
                
                # Generar nuevo folio
                new_consecutive = last_consecutive + 1
                self.folio = f"{prefix}{new_consecutive}"
            
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name='Encuenta'
        verbose_name_plural='Encuestas'


    # @property
    # def folio(self):
    #     if self.type == 'COMPLAINT':
    #         return f'Q-{self.id}'
        
    #     elif self.type == 'SUGGESTION':
    #         return f'S-{self.id}'
        
    #     elif self.type == 'CONGRATULATION':
    #         return f'F-{self.id}'
        

    #     return f'-{self.id}'
        


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

