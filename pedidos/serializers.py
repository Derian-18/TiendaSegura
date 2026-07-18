from rest_framework import serializers
from django.db import transaction
from .models import Pedido, ArticuloPedido
from productos.models import Producto


class ArticuloPedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = ArticuloPedido
        fields = ('id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario')
        read_only_fields = ('precio_unitario',)


class ArticuloPedidoInputSerializer(serializers.Serializer):
    """Serializer de solo entrada, usado al crear un pedido."""
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.filter(activo=True))
    cantidad = serializers.IntegerField(min_value=1)


class PedidoSerializer(serializers.ModelSerializer):
    articulos = ArticuloPedidoSerializer(many=True, read_only=True)
    usuario = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'estado', 'creado_en', 'articulos')
        read_only_fields = ('id', 'usuario', 'estado', 'creado_en')


class PedidoCreateSerializer(serializers.ModelSerializer):
    articulos = ArticuloPedidoInputSerializer(many=True, write_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'articulos')
        read_only_fields = ('id',)

    def validate_articulos(self, value):
        if not value:
            raise serializers.ValidationError("El pedido debe tener al menos un artículo.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        articulos_data = validated_data.pop('articulos')
        # El usuario del pedido siempre viene de request.user, nunca del body
        usuario = self.context['request'].user
        pedido = Pedido.objects.create(usuario=usuario)

        for item in articulos_data:
            producto = item['producto']
            ArticuloPedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=producto.precio,  # se congela el precio actual
            )
        return pedido

    def to_representation(self, instance):
        # Al responder, usamos el serializer de lectura completo
        return PedidoSerializer(instance, context=self.context).data