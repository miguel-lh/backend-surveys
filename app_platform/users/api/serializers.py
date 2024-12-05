from django.contrib.auth import password_validation
from django.contrib.auth.models import BaseUserManager

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from app_platform.users.models import User


class UserSerializer(serializers.ModelSerializer):
    # created = serializers.CharField(source='date_joined')

    class Meta:
        model = User
        fields = ("id", "date_joined", "name", "email", "is_active")

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        # }

class EmptySerializer(serializers.Serializer):
    class Meta:
        model = User
        exclude = (
            'username',
            'password',
            'last_login',
            'is_staff',
            'groups',
            'user_permissions',
            'is_superuser',
        )

class AuthUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'groups', 'user_permissions',
                    'date_joined', 'is_superuser')

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key  
    

class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'password',
        )

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Este usuario ya está registrado")

        user.usernemailame = value
        # The normalize_email method of BaseUserManager prevents different sign-ups of case sensitive email domains.
        # https://stackoverflow.com/questions/27936705/what-does-it-mean-to-normalize-an-email-address
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('No coincide la contraseña')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class ResetPasswordSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value