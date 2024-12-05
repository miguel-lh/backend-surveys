from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializers import UserSerializer, UserRegisterSerializer, AuthUserSerializer, UserLoginSerializer, PasswordChangeSerializer ,ResetPasswordSerializer, EmptySerializer
from .utils import get_and_authenticate_user, reset_password, create_user

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter,  filters.OrderingFilter, DjangoFilterBackend]
    ordering = ('-id')
    search_fields = ['name', 'email',]
    filterset_fields = { 'is_active', }
    # lookup_fi|eld = "pk"


class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny,]
    serializer_class = EmptySerializer
    serializer_classes = {
        'register': UserRegisterSerializer,
        'login': UserLoginSerializer,
        'password_change': PasswordChangeSerializer,
        'reset_password': ResetPasswordSerializer,
    }

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data,)
        instance = create_user(**serializer.validated_data)
        
        data = UserRegisterSerializer(instance).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated,])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

