from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        # Siempre se registra como 'cliente'. El rol admin se asigna manualmente
        # desde el panel de Django, nunca desde el registro público (seguridad).
        usuario = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'rol', 'date_joined')
        read_only_fields = ('id', 'rol', 'date_joined')