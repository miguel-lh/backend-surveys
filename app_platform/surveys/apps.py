from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfig):
    name = "app_platform.surveys"
    verbose_name = _("Encuestas")
