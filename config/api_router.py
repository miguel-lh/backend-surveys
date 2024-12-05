from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from app_platform.users.api.views import UserViewSet, AuthViewSet
from app_platform.surveys.api.views import SurveysViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("surveys", SurveysViewSet)
router.register("users", UserViewSet)
router.register("auth", AuthViewSet, basename='auth')


app_name = "api"
urlpatterns = router.urls
