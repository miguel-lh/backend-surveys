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

    name = models.CharField(_('Nombre'), max_length=2000)
    description = models.TextField(_('Descripcion'), null=True, blank=True)
    type = models.CharField(_('Tipo'), choices=TYPE_SURVEYS, )
    status = models.CharField(_('Tipo'), choices=STATUS_SURVEYS, default='IN_PROGRESS')
    phone = models.CharField(_('Telefono'), max_length=10)
    is_removed = models.BooleanField(_('Eliminado'), default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f'# {self.id}'
    
    class Meta:
        verbose_name='Encuenta'
        verbose_name_plural='Encuestas'


