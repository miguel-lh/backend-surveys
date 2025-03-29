from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Surveys

@receiver(pre_save, sender=Surveys)
def set_folio(sender, instance, **kwargs):

    print(instance.folio)
    if not instance.folio:
        instance.folio = Surveys.get_next_folio(instance.type)