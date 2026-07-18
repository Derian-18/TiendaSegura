from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'activo', 'creado_en')
        read_only_fields = ('id', 'creado_en')