from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
import re

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        # Verificar si el email ya está registrado
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está registrado.")
        
        # Validación del formato del correo
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("El correo electrónico no tiene un formato válido.")
        
        return value
