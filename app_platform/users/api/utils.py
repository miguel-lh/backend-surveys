# encoding: utf-8
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers


def create_user(password,  **extra_fields):
    user = get_user_model().objects.create_user(password=password, **extra_fields)
    return user

def get_and_authenticate_user(email, password):

    # username can be an email o phone_number backend / check auth_email_or_phone auth backend
    user = authenticate(email=email , password=password)

    if user is None:
        user = authenticate(email=email , password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username/password. Please try again!")
        
    if not user.is_active:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
        

    return user


def reset_password(user, new_password, **extra_fields):
    user = get_user_model().objects.filter(id=user)
    if not user:
        raise serializers.ValidationError("Invalid user. Please try again!")

    user = user.get()
    user.set_password(new_password)
    user.save()
    return user